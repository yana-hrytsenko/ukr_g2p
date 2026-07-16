# ukr_g2p — Ukrainian Grapheme-to-Phoneme Transcription

**Rule-based + neural G2P for Ukrainian.** Converts text into six transcription
modes (phonemic / broad / narrow, in both Ukrainian notation and IPA, plus an
English-friendly pronunciation guide) via **a transparent, declarative rule
pipeline** — not string hacking.

**[Live demo →](https://ukr-g2p.onrender.com)** (takes a minute to load; use Chromium-based browsers (Chrome, Edge))
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/License-Non--Commercial%20Research-orange)


<img width="385" height="196" alt="Screenshot 2026-07-16 091509" src="https://github.com/user-attachments/assets/dd6cc621-2f10-40b5-a1cc-a62cb938350b" />


### Why this is different

Most G2P tools mutate strings directly, hard-coding each phonological
process into procedural logic. Here, every process — assimilation,
gemination, vowel reduction — is a **typed, inspectable rule object**
applied to tokens carrying explicit phonological features. 
(See *ukr_g2p/src/ukr_g2p/modifications.py*)
Rules are data, not control flow:

```python
SOFTNESS_ASSIMILATION = CombinatoryModificationRule(
    name='softness_assim',
    type='assimilation',
    direction='regressive',
    patterns=[
        AssimilationPattern(
            trigger=phoneme_is('soft', 'dental'),
            target=phoneme_is('dental'),
            map=SOFT_PAIRS_MAP,
        )
    ]
)
```

Three cumulative passes (phonemic → broad → narrow) mean each level
inherits the previous one's changes, mirroring standard phonological
theory. A fine-tuned ByT5 model complements the rule engine for broad
IPA, occasionally beating it on stress prediction for out-of-dictionary
words.



**Jump to:** [Architecture](#architecture) · [Output Modes](#output-modes) ·
[Rules Covered](#phonological-rules-covered) · [Neural Model](#neural-model--byt5) ·
[Evaluation](#evaluation) · [Limitations](#limitations-and-future-work) ·
[Installation](#installation) · [Usage](#usage)

---

## Status

This project is under active improvement.

---

## Architecture

### Key design decisions

**Why not a traditional rewrite-rule system?**
Traditional phonological implementations often mutate strings directly.
This project instead represents phonological objects as tokens with
features, allowing multiple interacting rules without destructive
string operations.

**Declarative rules over procedural code.** Every phonological process
is a typed rule object (`CombinatoryModificationRule`,
`PositionalModificationRule`, `QuantitativeModificationRule`) with
explicit trigger conditions and propagation direction. Rules are data,
not logic — easy to inspect, modify, and extend without touching the
engine.

**Separate phonemic/broad/narrow layers.** Modifications are applied
in three cumulative passes. Each pass builds on the previous, so broad
output includes phonemic changes but not narrow detail. This mirrors
standard phonological theory and makes the system's behaviour
predictable.

**Token-based pipeline.** All phonological features (stress,
palatalization, length, labialization, fronting, nasalization) are
stored as attributes on token objects rather than embedded as special
characters in a string. This avoids the fragile string mutation
patterns common in earlier rule-based G2P implementations.

**Diagram.** Can be found in `ukr_g2p/doc`.

---

## Output Modes

The system distinguishes three levels of phonetic detail, each
available in Ukrainian notation, IPA, and English-friendly
romanization:

### Phonemic `/на'стрʹій/` `/'nɑstrʲij/`
The underlying phonological representation. No allophonic detail —
stressed and unstressed vowels are identical, only assymilations apply,
and phonemes appear in their base form.
Useful for linguistic analysis and as a reference level.

### Broad phonetic `[на'стрʹіĭ]` `['nɑstrʲii̯]`
Main allophones are shown. Stress affects vowel quality (unstressed `а → ɐ` etc.),
coda в and й become non-syllabic, fine-grained в allophony (`ʋ`, `w`, `ʍ`, `u̯`)
gemination is marked, and vowel reduction is indicated. This is the
most useful level for language learners and most practical applications.

### Narrow phonetic `[нã'стрʹіĭ]` `['n̪ɑ̃s̪t̪r̪ʲii̯]`
Full allophonic detail: dental diacritics on coronal consonants,
dark `ɫ` for hard л, nasalization on vowels adjacent to nasals,
labialization before round vowels, and fronting in palatal environments.

### English-friendly `<n-AH-s-t-r-ee-y>`
Approximate pronunciation using English letter combinations, with
stressed vowels in uppercase. Intended for English speakers with no
knowledge of IPA.

---

## Phonological Rules Covered

**Phonemic level**
- Regressive voicing assimilation (s→z before voiced consonants)
- Articulation assimilation (dental stops → affricates before sibilants)
- Softness assimilation (dental softness spreads to preceding dental)

**Broad level**
- Gemination (identical adjacent consonants → long consonant)
- Semi-palatalization (iotated vowels influence preceding semisoftable consonant)
- Vowel reduction (unstressed о, е, и shift toward adjacent quality)
- Coda allophony (в and й become non-syllabic in coda position)
- в allophony

**Narrow level**
- Labialization (consonants before round vowels acquire ʷ)
- Nasalization (vowels adjacent to m/n acquire nasal quality)
- Progressive and regressive fronting (vowels in palatal environments)
- Dental diacritics on coronal consonants
- Dark л (ɫ) for hard л

---

## Neural Model — ByT5

### Why ByT5

ByT5 operates directly on raw bytes — every character is its own input
unit, with no subword tokenizer. This makes it naturally suited for
G2P: the model reasons about individual graphemes without any
preprocessing, and handles Cyrillic script without special treatment.
Pretraining on multilingual data gives the model prior knowledge of
phonological patterns across many languages before fine-tuning on
Ukrainian specifically.

### Training data

Silver-standard training pairs were generated by running the rule-based
system on a Ukrainian wordlist, producing (word, IPA) pairs.

| Source | Count |
|--------|-------|
| Book corpus (non-unique) | ~250k tokens |

### Training

Fine-tuned from `google/byt5-small`.

Configuration:
- 5 training epochs
- AdamW optimizer (default Hugging Face configuration)
- Learning rate: 5e-5
- Batch size: 16
- 10% validation split
- Maximum sequence length: 32
- Best checkpoint selected by validation loss

The model learns a character-level mapping from Ukrainian orthography to
broad IPA representations using the ByT5 sequence-to-sequence architecture.

---

## Evaluation

Evaluated against a held-out set of ~2000 words from the kaikki.org
Ukrainian Wiktionary dump, excluded from training data.

### Metrics

| Metric | Rule-based | ByT5 |
|--------|-----------|------|
| PER (with stress) | 6.5% | 12.3% |
| PER (no stress) | 1.6% | 5.1% |
| **PER (no stress, no vowels) | 0.7% | 1.0% |**
| Exact match | 65.5% | 50.9% |
| Exact match (no stress) | 86.8% | 67.3% |
| **Exact match (no stress, no vowels) | 94.7% | 93.3% |**
| WER | 34.5% | 49.1% |

**Takeaway:** stress placement drives most of the error gap — once stress
and vowels are excluded, both systems land within 0.3 points of each other
(0.7% vs 1.0% PER), meaning the core consonantal transcription is solid in
both. The rule-based system currently wins on stress; ByT5 catches
out-of-dictionary words it doesn't.

### Interpretation

The rule-based system outperforms the first ByT5 model overall.
However, the results require careful interpretation — a significant
portion of the error in both systems is attributable to factors
outside the core transcription logic. The ByT5 model successfully
learned segmental pronunciation mapping from a rule-generated corpus.
Remaining errors were primarily related to lexical stress assignment,
which reflects a known challenge in Ukrainian pronunciation modeling.
**Future work will investigate a dedicated stress prediction component
using dictionary-based or neural approaches.**

**Stress placement** accounts for the largest share of errors.
Comparing PER with and without stress (6.5% → 1.6% for rules,
12.3% → 5.1% for ByT5) shows that roughly half of all character-level
errors are stress marks. The rule-based system relies on the
`ukrainian-word-stress` library which has incomplete coverage, and the
ByT5 model was not trained with a dedicated stress objective. A
dedicated stress prediction component is planned as a separate model.

**Vowel reduction cascades from stress errors** — when stress is placed
on the wrong syllable, full and reduced vowel forms are swapped
accordingly. The near-identical PER once both stress and vowels are
excluded (0.7% vs 1.0%) confirms that the core consonantal and
structural transcription is accurate in both systems — the errors are
concentrated in stress-dependent phenomena.

**Syllable-level vs token-level stress placement** — in some cases the
correct syllable is stressed but the IPA stress mark `ˈ` is placed
before the wrong token within that syllable. This is a known limitation
of the current `find_syllable_start` implementation and will be
addressed in a future version.

**Gold standard quality** — the Wiktionary IPA entries occasionally
contain errors or use non-standard conventions. Notably, some gold
entries mark semipalatalization on consonants as a result of assimilation
where Ukrainian phonological tradition does not — this inflates the apparent
error rate for both systems without reflecting genuine transcription mistakes.

### ByT5 — qualitative observations

Despite lower overall scores on this evaluation set, the ByT5 model
shows a notable advantage in stress prediction for words absent from
the `ukrainian-word-stress` library. In such cases the rule-based
system produces unstressed output (flat vowel quality throughout),
while ByT5 correctly identifies the stressed syllable — suggesting the
model has learned stress patterns from training data rather than
relying on lookup.

This is the first training run of the model on a silver-standard
dataset of ~250k words generated by ukr_g2p.

**Further work is planned:**
- A dedicated stress prediction model trained on a larger,
  stress-annotated corpus
- Fine-tuning on an expanded dataset currently in progress
- Retraining once syllable-level stress placement is corrected in
  the rule-based system, to produce cleaner training targets
- Formal evaluation after each improvement to track progress

The current results should be read as a baseline for a work in
progress rather than a final system evaluation.

---

## Limitations and Future Work

- **Stress model** — a dedicated stress prediction component would
  improve vowel reduction accuracy significantly. Currently dependent
  on the `ukrainian-word-stress` library, which has incomplete coverage.
- **Syllable detection** — syllable-level stress placement must be corrected
  in the rule-based system.
- **Optional assimilation**
- **Compound words** — the о linking vowel in compounds (водопровід/vodoprovid)
  is not exempted from vowel reduction rules.
- **Fixing occasional bugs**

---

## Installation

```bash
git clone https://github.com/yana-hrytsenko/ukr_g2p
cd ukr_g2p
pip install -r requirements.txt
```

## Usage

### CLI

```bash
ukr-g2p навчання
# [nɐ'u̯t͡ʃɑnʲ:ɐ]

ukr-g2p навчання --mode ukr_broad
# [наўчанʹ:а]

ukr-g2p навчання --mode all
# formatted block with all seven layers

ukr-g2p навчання --mode all --raw
# ukr_phonemic: навчанʹнʹа
# ukr_broad: наўчанʹ:а
# ...
```

Available modes: `ukr_phonemic`, `ukr_broad`, `ukr_narrow`, `ipa_phonemic`,
`ipa_broad` (default), `ipa_narrow`, `eng_friendly`, or `all`.

> If `ukr-g2p` isn't found after installing, use
> `python -m ukr_g2p` instead — same behavior, doesn't rely on your
> PATH.

### As a library

```python
from ukr_g2p import transcribe

transcribe("навчання", mode="ipa_broad")
# [nɐ'u̯t͡ʃɑnʲ:ɐ]

transcribe("навчання", mode="all", formatted=False)
# {'ukr_phonemic': ..., 'ipa_broad': ..., ...}
```

---

## References

- Xue et al. (2022) — [ByT5: Towards a Token-Free Future](https://arxiv.org/abs/2105.13626)
- Ylonen (2022) — [Wiktextract: Wiktionary as Machine-Readable Structured Data](https://aclanthology.org/2022.lrec-1.140)
- Ukrainian phonology reference: [Help:IPA/Ukrainian](https://en.wikipedia.org/wiki/Help:IPA/Ukrainian)

---

AI tools were used for parts of implementation support, debugging, and code refinement.
The linguistic analysis, rule design, model choices, dataset construction
and evaluation methodology were developed by the author.

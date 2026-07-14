# ukr_g2p — Ukrainian Grapheme-to-Phoneme Transcription

Convert Ukrainian text into phonemic, broad IPA, narrow IPA and English-friendly pronunciation.

A rule-based and neural G2P system for Ukrainian, producing three 
levels of phonetic transcription for both Ukrainian phonetic notation 
and IPA, plus an English-friendly pronunciation guide.

Originally developed as a thesis project, later extended with a 
declarative rule architecture, three transcription levels, and a 
fine-tuned ByT5 neural model for broad IPA.

---

## Quick Example

Input: **навчання**

ukr_phonemic : /навча'нʹнʹа/

ukr_broad    : [наўча'нʹ:а]

ukr_narrow   : [нãўчã'˙нʹ:˙ã]


ipa_phonemic : /nɑ'ʋt͡ʃɑnʲnʲɑ/

ipa_broad    : [nɐ'u̯t͡ʃɑnʲ:ɐ]

ipa_narrow   : [n̪ɐ̃'u̯t͡ʃɑ̟̃n̪ʲ:ɐ̟̃]


eng_friendly : n-ah-v-ch-AH-nj-ny-ah

---

## Status

This project is under active improvement.

## Overview

Ukrainian presents several challenges for G2P for automatic phonetic 
transcription — stress is unpredictable, palatalization is pervasive, 
and vowel quality shifts significantly in unstressed positions. Most 
existing tools produce a single flat IPA string with no distinction 
between phonemic and phonetic levels, and few existing Ukrainian G2P 
tools provide pronunciation guidance for English speakers.

This system produces six transcription modes across three levels of 
phonetic detail, implemented as a transparent rule pipeline where every 
phonological process is an inspectable, modifiable rule object. A 
fine-tuned ByT5 broad IPA model complements the rule system, and shows occasional
improvements in stress prediction — including words where the 
underlying stress library had no entry.

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

**Diagram** Can be found in ukr_g2p/doc.

---

## Output Modes

The system distinguishes three levels of phonetic detail, each 
available in Ukrainian notation, IPA, and English-friendly 
romanization:

### Phonemic `/на'стрʹій/` `/'nɑstrʲij/`
The underlying phonological representation. No allophonic detail — 
stressed and unstressed vowels are identical, assymilations apply,
and phonemes appear in their base form. 
Useful for linguistic analysis and as a reference level.

### Broad phonetic `[на'стрʹіĭ]` `['nɑstrʲii̯]`
Main allophones are shown. Stress affects vowel quality (nstressed `а → ɐ` etc.), 
coda в and й become non-syllabic, fine-grained в allophony (`ʋ`, `w`, `ʍ`, `u̯`)
gemination is marked, and vowel reduction is indicated. This is the 
most useful level for language learners and most practical applications.

### Narrow phonetic `[нã'стрʹіĭ]` `['n̪ɑ̃s̪t̪r̪ʲii̯]`
Full allophonic detail: dental diacritics on coronal consonants, 
dark `ɫ` for hard л, nasalization on vowels adjacent to nasals, 
labialization before round vowels, fronting in palatal environments, 
and .

### English-friendly `<n-AH-s-t-r-ee-y>`
Approximate pronunciation using English letter combinations, with 
stressed vowels in uppercase. Intended for English speakers with no 
knowledge of IPA.

---

## Phonological Rules Covered

**Phonemic level**
- Regressive voicing assimilation (s→z before voiced consonants)
- Articulation assimilation (dental stops → affricates before sibilants)
- Softness assimilation (dental softness spreads to preceeding dental)

**Broad level**
- Gemination (identical adjacent consonants → long consonant)
- Semi-palatalization (iotated vowels influence preceding semisoftable consonant)
- Vowel reduction (unstressed о, е, и shift toward adjacent quality)
- Coda allophony (v and j become non-syllabic in coda position)
- v allophony

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


## Evaluation

Evaluated against a held-out set of ~2000 words from the kaikki.org 
Ukrainian Wiktionary dump, excluded from training data.

### Metrics

| Metric | Rule-based | ByT5 |
|--------|-----------|------|
| PER (with stress) | 6.5% | 12.3% |
| PER (no stress) | 1.6% | 5.1% |
| PER (no stress, no vowels) | 0.7% | 1.0% |
| Exact match | 65.5% | 50.9% |
| Exact match (no stress) | 86.8% | 67.3% |
| Exact match (no stress, no vowels) | 94.7% | 93.3% |
| WER | 34.5% | 49.1% |

### Interpretation

The rule-based system outperforms the first ByT5 model overall. 
However, the results require careful interpretation — a significant 
portion of the error in both systems is attributable to factors 
outside the core transcription logic.The ByT5 model successfully 
learned segmental pronunciation mapping from a rule-generated corpus. 
Remaining errors were primarily related to lexical stress assignment, 
which reflects a known challenge in Ukrainian pronunciation modeling. 
Future work will investigate a dedicated stress prediction component 
using dictionary-based or neural approaches.:

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
entries mark semipalatalization on consonants as a result of assymilation 
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
dataset of ~250k words. 

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
- **Syllable detection** - syllable-level stress placement must be corrected 
  in the rule-based system.
- **Optional assymilation**
- **Compound words** — the о linking vowel in compounds (водопровід/vodoprovid) 
  is not exempted from vowel reduction rules.


---

## Installation

```bash
git clone https://github.com/yana-hrytsenko/ukr_g2p
cd ukr_g2p
pip install -r requirements.txt
```


## Usage

```python
from ukr_g2p import transcribe

transcribe("навчання", mode="ipa_broad")
# [nɐ'u̯t͡ʃɑnʲ:ɐ]

transcribe("навчання", mode="all", formatted=False)
# returns dict with all seven modes
```

---

## References

- Xue et al. (2022) — [ByT5: Towards a Token-Free Future](https://arxiv.org/abs/2105.13626)
- Ylonen (2022) — [Wiktextract: Wiktionary as Machine-Readable Structured Data](https://aclanthology.org/2022.lrec-1.140)
- Ukrainian phonology reference: [Help:IPA/Ukrainian](https://en.wikipedia.org/wiki/Help:IPA/Ukrainian)

- to be added







AI tools were used for parts of implementation support, debugging, and code refinement. 
The linguistic analysis, rule design, model choices, dataset construction
and evaluation methodology were developed by the author.





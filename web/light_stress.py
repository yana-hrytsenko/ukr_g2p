"""
Lightweight, Stanza-free alternative to ukrainian_word_stress.Stressifier.

The full Stressifier loads a ~500MB Stanza NLP pipeline (tokenize + POS +
mwt) purely to disambiguate heteronyms -- words with identical spelling
but different stress depending on grammatical role (e.g. блохи vs блохи
with different accents). That pipeline is too heavy for small/free
hosting tiers, and merely IMPORTING stanza also imports torch, which by
itself costs 300-500MB of RSS before anything runs.

This module avoids importing the `ukrainian_word_stress` *package* at
all (its __init__.py unconditionally imports stanza), and instead:
  - locates the package's data/stress.trie file directly on disk
    (via importlib.util.find_spec, which does not execute __init__.py)
  - loads it with marisa_trie (a lightweight pure dependency, ~12MB file)
  - reimplements the small, stanza-free tag-decoding logic that the
    library itself uses internally (see ukrainian_word_stress/tags.py
    and stressify_.py:_parse_dictionary_value / find_accent_positions)

Ambiguous words (a small minority) are left unstressed, matching the
library's own default OnAmbiguity.Skip behavior for unresolved cases.
Single-vowel words missing from the dictionary get stressed via a
simple heuristic, matching ukr_g2p.stress's own fallback.

Drop this file next to app.py and wire it in without touching the
package's own stress.py:

    import ukr_g2p.pipeline as _pipeline
    from light_stress import light_stress
    _pipeline.stress = light_stress
"""

import importlib.util
import os
import re

import marisa_trie

STRESS = '\u0301'  # combining acute accent -- matches ukr_g2p.symbols.STRESS

_WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)
_VOWELS = set('іиаоуеяюєї')

_POS_SEP = b'\xFE'
_REC_SEP = b'\xFF'


def _find_trie_path():
    """Locate ukrainian_word_stress's bundled trie file without
    importing the package (which would pull in stanza -> torch)."""
    spec = importlib.util.find_spec("ukrainian_word_stress")
    if spec is None or not spec.submodule_search_locations:
        raise ImportError("ukrainian_word_stress is not installed")
    pkg_dir = list(spec.submodule_search_locations)[0]
    return os.path.join(pkg_dir, "data", "stress.trie")


_trie = None
_TRIE_PATH = _find_trie_path()  # resolved now, while sys.modules is still clean


def _get_trie():
    global _trie
    if _trie is None:
        _trie = marisa_trie.BytesTrie()
        _trie.load(_TRIE_PATH)
    return _trie


def _parse_dictionary_value(value):
    """Reimplementation of ukrainian_word_stress.stressify_._parse_dictionary_value,
    stanza-free."""
    if _REC_SEP not in value:
        return [([], [int(b) for b in value])]
    entries = []
    for item in value.split(_REC_SEP):
        if item:
            accents_bytes, _, _tags_bytes = item.partition(_POS_SEP)
            entries.append(([int(b) for b in accents_bytes], [int(b) for b in accents_bytes]))
    return entries


def _accent_positions(trie, word):
    """Reimplementation of find_accent_positions, without POS
    disambiguation (we never have POS tags without Stanza -- ambiguous
    words are simply skipped, same as the library's own default)."""
    for candidate in (word, word.lower(), word.title()):
        if candidate in trie:
            values = trie[candidate]
            break
    else:
        return []

    entries = _parse_dictionary_value(values[0])
    if not entries:
        return []
    if len(entries) == 1:
        return entries[0][1]

    # multiple valid accents and no POS info to disambiguate -> skip
    return []


def _stress_word(word):
    positions = _accent_positions(_get_trie(), word)

    if not positions:
        vowel_positions = [i for i, ch in enumerate(word) if ch.lower() in _VOWELS]
        if len(vowel_positions) == 1:
            positions = [vowel_positions[0] + 1]
        else:
            return word

    for pos in sorted(positions, reverse=True):
        word = word[:pos] + STRESS + word[pos:]
    return word


def light_stress(text):
    """Drop-in replacement for ukr_g2p.stress.stress(), without Stanza."""
    return _WORD_RE.sub(lambda m: _stress_word(m.group(0)), text)


class LiteStressifier:
    """Callable matching ukrainian_word_stress.Stressifier's interface
    (`stressifier(text) -> stressed text`), including accepting the same
    `stress_symbol` constructor kwarg (ignored -- we always use the
    combining acute accent, matching ukr_g2p.symbols.STRESS)."""

    def __init__(self, stress_symbol=None):
        self.stress_symbol = stress_symbol

    def __call__(self, text):
        return light_stress(text)


class _FakeStressSymbol:
    AcuteAccent = "´"
    CombiningAcuteAccent = STRESS


def install_lite_stub():
    """Stub out the real `ukrainian_word_stress` package in sys.modules
    BEFORE ukr_g2p is imported.

    ukr_g2p/stress.py does `import ukrainian_word_stress` and builds a
    full Stressifier() *at module import time* (`stressifier =
    try_load_stressifier()`), which is what actually triggers the
    ~500MB Stanza + torch load -- monkeypatching stress.stressifier
    *after* import is too late, the memory is already spent. Installing
    this stub first makes stress.py's own import resolve to our
    lightweight substitute instead, so the heavy pipeline is never
    built in the first place. Must be called before any `import
    ukr_g2p` (or `from ukr_g2p import ...`) anywhere in the process.
    """
    import sys
    import types

    if isinstance(sys.modules.get("ukrainian_word_stress"), types.ModuleType) \
            and getattr(sys.modules["ukrainian_word_stress"], "_is_lite_stub", False):
        return  # already installed

    stub = types.ModuleType("ukrainian_word_stress")
    stub.Stressifier = LiteStressifier
    stub.StressSymbol = _FakeStressSymbol
    stub._is_lite_stub = True
    sys.modules["ukrainian_word_stress"] = stub
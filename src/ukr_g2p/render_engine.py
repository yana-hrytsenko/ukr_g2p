from dataclasses import dataclass
from .utils import *
from .phonemas import *


@dataclass
class RenderPattern:
    condition: object   
    output:    object   
    position:  str = "inline" 



# =============================================================================
# RENDERING
# =============================================================================

def char_is(*chars):
    return lambda t, ctx: t.char in chars

def token_is(*features):
    return lambda t, ctx: all(f in t.features for f in features)

def has(attr):
    return lambda t, ctx: bool(getattr(t, attr, None))

def has_mod(*names):
    return lambda t, ctx: all(n in t.modifications for n in names)

def allophone_is(*values):
    return lambda t, ctx: t.allophone in values

def from_map(mapping):
    return lambda t, ctx: mapping[t.char]

def add(char):
    return lambda t, ctx: char

def stress_mark():
    return lambda t, ctx: "'" if t.stress else ""

def uppercase():
    return lambda t, ctx: ctx.get('current_replace', t.char).upper()

def both(*predicates):
    return lambda t, ctx: all(p(t, ctx) for p in predicates)

def either(*predicates):
    return lambda t, ctx: any(p(t, ctx)for p in predicates)

def NOT(pred):
    return lambda t, ctx: not pred(t, ctx)


from .syllables import syllable_onsets

def find_syllable_start(tokens, stressed_index):
    """
    Finds the onset of the stressed syllable according to Ukrainian
    syllable-division rules (see syllables.py). Returns the token
    index where IPA stress should be placed.
    """
    start = stressed_index
    while start > 0 and tokens[start - 1].char not in WORD_EDGE:
        start -= 1
    end = stressed_index
    while end < len(tokens) and tokens[end].char not in WORD_EDGE:
        end += 1

    onsets = syllable_onsets(tokens, start, end)
    onset = start
    for o in onsets:
        if o <= stressed_index:
            onset = o
        else:
            break
    return onset

def after_soft_before_vowel():
    return lambda t, ctx: (
        t.palatalization and
        t.char != "й" and
        ctx["next"] is not None and
        ctx["next"].char in VOWELS and
        ctx["next"].char not in {"і", "и"}
    )

def after_soft_before_hard():
    return lambda t, ctx: (
        t.palatalization and
        t.char != "й" and
        ctx["next"] is not None and
        (ctx["next"].char in CONSONANTS or
        ctx["next"].char in WORD_EDGE)
    )

def resolve_surface(token):
    if token.allophone is not None:
        return token.allophone
    return token.char

def add_diacritic(base, mark):
    if mark == "̪":
        replacements = {
            "d͡z": f"d{mark}͡z{mark}",
            "t͡s": f"t{mark}͡s{mark}",
            "d͡ʒ": f"d{mark}͡ʒ{mark}",
            "t͡ʃ": f"t{mark}͡ʃ{mark}",
        }
        if base in replacements:
            return replacements[base]
    for symbol in ("ʲ"):
        if base.endswith(symbol):
            return base[:-len(symbol)] + mark + symbol
    return base + mark


def render(tokens, rules, ipa_stress=False, hyphenate=False):
    stress_positions = {}
    if ipa_stress:
        for i, token in enumerate(tokens):
            if token.stress and token.token_is('vowel'):
                onset = find_syllable_start(tokens, i)
                stress_positions[onset] = True
    parts = []
    for i, token in enumerate(tokens):
        if token.has("long_start"):
            continue
        if i in stress_positions:
            parts.append("'")
        base = resolve_surface(token)
        before = []
        replace = None
        add = []
        after = []
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        ctx = {
            "next": nxt,
            "index": i,
            "tokens": tokens
        }
        for rule in rules:
            if rule.condition(token, ctx):
                value = rule.output(token, ctx)
                #if value == "":     
                    #continue
                if rule.position == "after":
                    if isinstance(value, list):
                        after.extend(value)
                    else:
                        after.append(value)
                elif rule.position == "replace":
                    replace = value
                    ctx['current_replace'] = replace
                elif rule.position == "add":
                    add.append(value)
                elif rule.position == "before":
                    if isinstance(value, list):
                        before.extend(value)
                    else:
                        before.append(value)
        if replace is not None:
            base = replace
        for value in add:
            base = add_diacritic(base, value)
        '''result.extend(before)
        result.append(base)
        result.extend(after)'''
        chunk = ''.join(before) + base + ''.join(after)
        parts.append(chunk)
    if hyphenate:
        result = []
        current_word = []
        for part in parts:
            if part in WORD_EDGE:
                if current_word:
                    result.append('-'.join(current_word))
                    current_word = []
                result.append(part)
            else:
                current_word.append(part)
        if current_word:
            result.append('-'.join(current_word))
        return ''.join(result)
    return ''.join(parts)
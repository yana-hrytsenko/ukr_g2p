from dataclasses import dataclass
from .token import Token
from .phonemas import PHONES
from .mappings import IOTATION_MAP




@dataclass
class ParsePattern:
    trigger: object
    output:  object
    consume: int 



# =============================================================================
# rules.py  —  rule types + indexed engine
# =============================================================================


def make_phoneme(char, source=None, **kwargs):
    token = Token(char=char, features=set(PHONES.get(char, [])))
    if source is not None:
        token.stress = source.stress
    for key, value in kwargs.items():
        setattr(token, key, value)
    return token

def has_feature(feature):
    return lambda g, nxt: feature in PHONES.get(g.char, ())

def grapheme_is(*chars):
    return lambda g, nxt: g.char in chars

def sequence_is(*chars):
    return lambda g, nxt: (nxt and (g.char, nxt.char) == chars)

def next_is(char):
    return lambda g, nxt: (nxt and nxt.char == char)

def grapheme_in(chars):
    return lambda g, nxt: (g.char in chars)

def next_in(chars):
    return lambda g, nxt: (nxt and nxt.char in chars)

def either(*predicates):
    return lambda g, nxt: any(p(g, nxt) for p in predicates)

def both(*predicates):
    return lambda g, nxt: all(p(g, nxt) for p in predicates)


def parse(graphemes, rules):
    phonemes = []
    i = 0
    while i < len(graphemes):
        g = graphemes[i]
        nxt = graphemes[i + 1] if i + 1 < len(graphemes) else None
        matched = False
        for pattern in rules:
            if pattern.trigger(g, nxt):
                if callable(pattern.output):
                    result = pattern.output(g, nxt)
                else:
                    result = pattern.output
                result = [
                    p if isinstance(p, Token) else make_phoneme(p)
                    for p in result
                ]
                source_stress = g.stress or (pattern.consume >= 2 and nxt is not None and nxt.stress)
                if source_stress and result:
                    for phoneme in result:
                        phoneme.stress = False
                    target = None
                    if g.stress:
                        target = next((p for p in result if p.token_is("vowel") and p.char == g.char), None)
                    if target is None:
                        for phoneme in reversed(result):
                            if phoneme.token_is("vowel"):
                                target = phoneme
                                break
                    if target is not None:
                        target.stress = True
                    else:
                        result[-1].stress = True
                phonemes.extend(result)
                i += pattern.consume
                matched = True
                break
        if not matched:
            phonemes.append(make_phoneme(g.char, source=g))
            i += 1
    return phonemes


def apostrophe_iotation(g, nxt):
    base = IOTATION_MAP[nxt.char]
    return [
        make_phoneme('й'),
        make_phoneme(base)
    ]

def vowel_iotation(g, nxt):
    base = IOTATION_MAP[nxt.char]
    return [
        make_phoneme(g.char),
        make_phoneme('й'),
        make_phoneme(base)
    ]

def soft_consonant(g, nxt):
    base = IOTATION_MAP[nxt.char]
    return [
        make_phoneme(g.char + 'ʹ', palatalization=True),
        make_phoneme(base)
    ]

def semisoft_consonant(g, nxt):
    base = IOTATION_MAP[nxt.char]
    phoneme = make_phoneme(g.char, palatalization=True)
    phoneme.modifications.add("semipalatalization")
    return [phoneme, make_phoneme(base)]


def iotate(g, nxt):
    base = IOTATION_MAP[g.char]
    return [
        make_phoneme('й'),
        make_phoneme(base)
    ]


def soften_before_i(g, nxt):
    return [
        make_phoneme(g.char + "ʹ", palatalization=True),
        #make_phoneme('і')
    ]

def soften_before_softness_sign(g, nxt):
    return [
        make_phoneme(g.char + "ʹ", palatalization=True)
    ]
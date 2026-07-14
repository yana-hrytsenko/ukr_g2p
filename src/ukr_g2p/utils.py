import re
from .symbols import * 

def mark_prefix_d_boundary(text):
    for pref in sorted(D_PREFIXES, key=len, reverse=True):
        text = re.sub(rf'\b{pref}', pref + D_BOUNDARY, text)
    return text

def mark_apostrophe(text):
    text = text.replace("'", APOSTROPHE)
    return text


# =============================================================================
# navigation helpers
# =============================================================================
 
HARD_STOP  = {MINOR_PAUSE, MAJOR_PAUSE, '\n'} 
WORD_EDGE  = {MINOR_PAUSE, MAJOR_PAUSE, '\n', ' '} 

def next_token(tokens, i, stop=HARD_STOP, skip={' '}):
    j = i + 1
    while j < len(tokens):
        c = tokens[j].char
        if c in stop:
            return None, None
        if c in skip:
            j += 1
            continue
        return tokens[j], j
    return None, None

def prev_token(tokens, i, stop=HARD_STOP, skip={' '}):
    j = i - 1
    while j >= 0:
        c = tokens[j].char
        if c in stop:
            return None, None
        if c in skip:
            j -= 1
            continue
        return tokens[j], j
    return None, None


def next_syllable_stressed(tokens, i, stop=HARD_STOP, skip={' '}):
    j = i + 1
    while j < len(tokens):
        token = tokens[j]
        if token.char in stop:
            return False
        if token.char in skip:
            j += 1
            continue
        if token._is('vowel'):
            return token.stress
        j += 1
    return False

def stressed_vowel_is_high(tokens, i, stop=HARD_STOP, skip={' '}):
    j = i + 1
    while j < len(tokens):
        token = tokens[j]
        if token.char in stop:
            return False
        if token.char in skip:
            j += 1
            continue
        if token._is('vowel'):
            return token._is('high')
        j += 1
    return False
 



# =============================================================================
# modifications_helpers.py  
# =============================================================================

def NOT(fn):
    return lambda t, p, n: not fn(t, p, n)

def BOTH(*predicates):
    return lambda t, p, n: all(
        predicate(t, p, n) for predicate in predicates
    )

def EITHER(a, b):
    return lambda t, p, n: a(t, p, n) or b(t, p, n)

def identical_consonants(a, b):
    return (
        a is not None and
        b is not None and
        a.char == b.char and
        "consonant" in a.features and
        "consonant" in b.features
    )
                    
def from_map(mapping):
    return lambda t: mapping[t.char]

def coda_position(token, prv, nxt):
    return (
        (prv is None or prv.token_is('vowel')) and
        (nxt is None or nxt.token_is('consonant')) and
        not (prv is None and nxt is None) and
        not (prv is None and token.char == 'в') and
        not identical_consonants(token, nxt) and
        not token.long_start 
    )

def after_vowel(token, prv, nxt):
    return prv and prv.token_is('vowel')

def before_voiceless(token, prv, nxt):
    return nxt and nxt.token_is('voiceless')

def before_round_vowel(token, prv, nxt):
    return nxt and nxt.token_is('vowel') and nxt.token_is('round')

def before_voiced_consonant(token, prv, nxt):
    return nxt and nxt.token_is('consonant') and nxt._is_not('voiceless')

def except_v(token, prv, nxt):
    return nxt and nxt.char != 'в'

def stressed(token, prv, nxt):
    return token.has('stress')

def next_vowel(token):
    for t in token.tokens[token.index + 1:]:
        if t.token_is('vowel'):
            return t
    return None

def before_stressed_high_vowel(token, prv, nxt):
    v = next_vowel(token)
    return (
        v and
        v.has('stress') and
        v.token_is('high')
    )
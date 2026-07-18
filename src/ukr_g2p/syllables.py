from .symbols import WORD_EDGE


# =============================================================================
# syllables.py  —  Ukrainian syllable division (складоподіл)
# =============================================================================
#
# Implements the standard складоподіл rule set:
#   - a single consonant between vowels always starts the next syllable
#   - a sonorant consonant (й, в, р, л, м, н) at the head of a 2+
#     consonant cluster stays with the PRECEDING syllable; the rest of
#     the cluster moves to the following syllable as one block
#   - a voiced obstruent immediately followed by a voiceless obstruent
#     splits between syllables (the voiced one stays previous)
#   - identical/doubled consonants always move together to the next
#     syllable
#   - everything else -- same-voicing obstruent pairs (which is why the
#     fixed ск/ст/сп/зд/шч clusters never split: с+к, с+т, etc. are
#     just same-voicing pairs), an obstruent followed by a sonorant,
#     and any other combination -- moves together to the next syllable
#
# These few rules, applied to just the first two consonants of each
# inter-vowel cluster, reproduce the full rule set (including the
# separate-looking rules for 3- and 4-consonant clusters): at most one
# leading consonant ever peels off to the previous syllable, and
# everything after it always bundles into the next syllable.


def is_vowel(token):
    return token.token_is('vowel')

def is_sonorant(token):
    return token.token_is('sonorant')

def is_voiced_obstruent(token):
    return token.token_is('voiced')

def is_voiceless_obstruent(token):
    return token.token_is('voiceless')


def cluster_split(cluster):
    """
    Given the consonant tokens between two vowels, return how many of
    them (counted from the start) attach to the PRECEDING syllable.
    Everything else attaches to the FOLLOWING syllable as one block.
    """
    if len(cluster) < 2:
        return 0

    c0, c1 = cluster[0], cluster[1]

    if c0.char == c1.char:
        return 0
    if is_sonorant(c0):
        return 1
    if is_voiced_obstruent(c0) and is_voiceless_obstruent(c1):
        return 1
    return 0


def syllable_onsets(tokens, start=0, end=None):
    """
    Return the token indices where each syllable begins, within
    tokens[start:end] (a single word-boundary-delimited span).
    """
    if end is None:
        end = len(tokens)

    vowels = [i for i in range(start, end) if is_vowel(tokens[i])]
    if not vowels:
        return []

    onsets = [start]
    prev_vowel = vowels[0]

    for v in vowels[1:]:
        cluster = tokens[prev_vowel + 1:v]
        split = cluster_split(cluster)
        onsets.append(prev_vowel + 1 + split)
        prev_vowel = v

    return onsets


def make_syllables(tokens):
    """
    Split a full token stream (possibly multiple words, punctuation-
    delimited) into syllables. Returns a list of (start, end) index
    pairs, each spanning one syllable's tokens.
    """
    syllables = []
    word_start = None

    def flush(word_end):
        onsets = syllable_onsets(tokens, word_start, word_end)
        for i, onset in enumerate(onsets):
            end = onsets[i + 1] if i + 1 < len(onsets) else word_end
            syllables.append((onset, end))

    for i, token in enumerate(tokens):
        if token.char in WORD_EDGE:
            if word_start is not None:
                flush(i)
                word_start = None
        elif word_start is None:
            word_start = i

    if word_start is not None:
        flush(len(tokens))

    return syllables
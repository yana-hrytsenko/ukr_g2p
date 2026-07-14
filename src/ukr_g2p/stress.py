import re
import ukrainian_word_stress
from .symbols import STRESS

# =============================================================================
# STRESS
# =============================================================================


def try_load_stressifier():
    try:
        from ukrainian_word_stress import Stressifier, StressSymbol
        return Stressifier(stress_symbol=StressSymbol.CombiningAcuteAccent)
    except Exception:
        return None

stressifier = try_load_stressifier()
VOWELS = set('іиаоуеяюєї')

def add_monosyllable_stress(word):
    vowel_count = sum(char in VOWELS for char in word)
    if vowel_count != 1:
        return word
    return ''.join(
        char + STRESS if char in VOWELS else char for char in word
    )

def add_stress(word):
    if stressifier is not None:
        try:
            stressed =  stressifier(word)
            if STRESS not in stressed:
                stressed = add_monosyllable_stress(stressed)
            return stressed
        except Exception:
            pass
    return add_monosyllable_stress(word)

def stress(text):
    parts = re.split(r'(//|/|\s+|[,.!?;:])', text)
    result = []
    for part in parts:
        if part.strip() == '' or not any(c in VOWELS for c in part):
            result.append(part)
        else:
            result.append(add_stress(part))
    return ''.join(result)

    
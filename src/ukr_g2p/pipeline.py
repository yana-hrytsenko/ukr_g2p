from copy import deepcopy
from .normalise import preprocess
from .exceptions import exceptions
from .stress import *
from .annotate import *
from .tokenizer import tokenize
from .parser import PARSING_RULES
from .parse_engine import parse
from .modifications import PHONEMIC_RULES, BROAD_RULES, NARROW_RULES, MODIFICATION_RULES
from .rules_engine import apply_modifications
from .render import *
from .render_engine import render
from .stress import *



# =============================================================================
# PIPELINE
# =============================================================================

def apply_stage(tokens, rules):
        for rule in rules:
            tokens = rule(tokens)
        return tokens


def build_pipeline(text):

    text =     preprocess(text)
    text =     stress(text)
    text =     exceptions(text)
    text =     annotate(text)
    tokens =   tokenize(text)
    phonemes = parse(tokens, PARSING_RULES)
    
    phonemic_tokens = apply_modifications(deepcopy(phonemes),        PHONEMIC_RULES)
    broad_tokens =    apply_modifications(deepcopy(phonemic_tokens), BROAD_RULES)
    narrow_tokens =   apply_modifications(deepcopy(broad_tokens),    NARROW_RULES)

    return phonemic_tokens, broad_tokens, narrow_tokens


# =============================================================================
# MAIN API
# =============================================================================

def transcribe(text, mode="ipa_broad", formatted=True):

    phonemic_tokens, broad_tokens, narrow_tokens = build_pipeline(text)


    RENDER_RULES = {
     
    "ukr_phonemic": (phonemic_tokens, UKR_PHONEMIC_RENDER),
    "ukr_broad":    (broad_tokens,    UKR_BROAD_RENDER),
    "ukr_narrow":   (narrow_tokens,   UKR_NARROW_RENDER),

    "ipa_phonemic": (phonemic_tokens, IPA_PHONEMIC_RENDER),
    "ipa_broad":    (broad_tokens,    IPA_BROAD_RENDER),
    "ipa_narrow":   (narrow_tokens,   IPA_NARROW_RENDER),

    "eng_friendly": (phonemic_tokens, ENG_FRIENDLY_RENDER),

    }   

    # ALL MODES OUTPUT
    if mode == "all":
        results = {
            key: render(tokens, rules, ipa_stress=key.startswith('ipa'), hyphenate=key.startswith('eng'))
            for key, (tokens, rules) in RENDER_RULES.items()
        }
        if not formatted:
            return results
        return (
            f"Word: {preprocess(stress(text))}\n\n"
            f"ukr_phonemic : /{results['ukr_phonemic']}/\n"
            f"ukr_broad    : [{results['ukr_broad']}]\n"
            f"ukr_narrow   : [{results['ukr_narrow']}]\n\n"
            f"ipa_phonemic : /{results['ipa_phonemic']}/\n"
            f"ipa_broad    : [{results['ipa_broad']}]\n"
            f"ipa_narrow   : [{results['ipa_narrow']}]\n\n"
            f"eng_friendly : <{results['eng_friendly']}>\n\n"
            f"{'='*40}\n"
        )
    
    # SINGLE MODE OUTPUT
    if mode not in RENDER_RULES:
        raise ValueError(f"Unknown mode: {mode}")
    tokens, rules = RENDER_RULES[mode]
    return render(tokens, rules, ipa_stress=mode.startswith('ipa'), hyphenate=mode.startswith('eng')) 


import re
from .symbols import *
from .mappings import *
from .render_engine import RenderPattern, has, stress_mark, has_mod, allophone_is, token_is, from_map, both, either, NOT, char_is, uppercase, after_soft_before_vowel, after_soft_before_hard


# =============================================================================
# RENDERING
# =============================================================================

def compose(*layers):
    result = []
    for layer in layers:
        result.extend(layer)
    return result

def literal(char):
    return lambda t, ctx: char


# =============================================================================
# UKR PHONEMIC 
# =============================================================================

UKR_PHONEMIC = [
    
    RenderPattern(
        condition=has("stress"),
        output=stress_mark(),
        position="after"
    )

]


# =============================================================================
# UKR BROAD 
# =============================================================================

UKR_BROAD = [

    RenderPattern(
        condition=char_is("й"),
        output=literal("j"),
        position="replace"
    ),

    RenderPattern(
        condition=allophone_is("ĭ"),
        output=literal('ĭ'),
        position="replace"
    ),

    RenderPattern(
        condition=has_mod("semipalatalization"),
        output=literal("’"),
        position="after"
    ),

    RenderPattern(
        condition=has("long_end"),
        output=literal(":"),
        position="after"
    ),
    
    RenderPattern(
        condition=has("long_start"),
        output=literal(''),
        position="replace"
    ),

    RenderPattern(
        condition=allophone_is("и"),
        output=literal("ᵉ"),
        position="after"
    ),

    RenderPattern(
        condition=allophone_is("е"),
        output=literal("ᵘ"),
        position="after"
    ),

    RenderPattern(
        condition=allophone_is("о"),
        output=literal("ʸ"),
        position="after"
    )

]


# =============================================================================
# UKR NARROW 
# =============================================================================

UKR_NARROW = [
    
    RenderPattern(
        condition=has_mod("fronting_left"),
        output=literal("˙"),
        position="before"
    ),

    RenderPattern(
        condition=has_mod("fronting_right"),
        output=literal("˙"),
        position="after"
    ),

    RenderPattern(
        condition=has_mod("labialization"),
        output=literal("˚"),
        position="after"
    ),

    RenderPattern(
        condition=has_mod("nasalization"),
        output=from_map(NASALIZATION_MAP),
        position="replace"
    )  

] 



# =============================================================================
# IPA PHONEMIC
# =============================================================================

IPA_PHONEMIC = [

    RenderPattern(
        condition=token_is("vowel"),
        output=from_map(IPA_VOWELS_STRESSED),
        position="replace"
    ),

    RenderPattern(
        condition=token_is("consonant"),
        output=from_map(IPA_CONS),
        position="replace"
    )

]


# =============================================================================
# IPA BROAD
# =============================================================================

IPA_BROAD = [

    RenderPattern(
        condition=has_mod("semipalatalization"),
        output=literal("ʲ"),
        position="after"
    ),

    RenderPattern(
        condition=has("long_start"),
        output=literal(''),
        position="replace"
    ),

    RenderPattern(
        condition=has("long_end"),
        output=literal(":"),
        position="after"
    ),

    RenderPattern(
        condition=either(char_is('л')),
        output=from_map(DARK_L),
        position="replace"
    ),

    RenderPattern(
        condition=both(token_is('vowel'), NOT(has('stress'))),
        output=from_map(IPA_VOWELS_UNSTRESSED),
        position="replace"
    ),

    RenderPattern(
        condition=allophone_is("о"),
        output=literal('o'),
        position="replace"
    ),

    RenderPattern(
        condition=allophone_is("е", "и"),
        output=literal('e'),
        position="replace"
    ),

    RenderPattern(
        condition=allophone_is("ĭ"),
        output=literal('i̯'),
        position="replace"
    ),

    RenderPattern(
        condition=allophone_is("ў"),
        output=literal('u̯'),
        position="replace"
    ),

    RenderPattern(
        condition=allophone_is('w'),
        output=literal('w'),
        position='replace'
    ),

    RenderPattern(
        condition=allophone_is('ʍ'),
        output=literal('ʍ'),
        position='replace'
    )

]


# =============================================================================
# IPA NARROW
# =============================================================================

IPA_NARROW = [


    RenderPattern(
        condition=either(token_is('dental'), token_is('alveolar')),
        output=literal("̪"),
        position="add"
    ),

    
    RenderPattern(
        condition=either(has_mod("fronting_left"), has_mod("fronting_right")),
        output=literal('̟'),
        position="add"
    ),

    RenderPattern(
        condition=has_mod("labialization"),
        output=literal("ʷ"),
        position="after"
    ),

    RenderPattern(
        condition=has_mod("nasalization"),
        output=literal('̃'),
        position="add"
    )  

] 

# =============================================================================
# ENGLISH FRIENDLY
# =============================================================================

ENG_FRIENDLY = [

    RenderPattern(
        condition=token_is('vowel'),
        output=from_map(ENG_FRIEND_VOWELS),
        position="replace"
    ),

    RenderPattern(
        condition=token_is("consonant"),
        output=from_map(ENG_FRIEND_CONS),
        position="replace"
    ),
    
    RenderPattern(
        condition=after_soft_before_vowel(),
        output=literal('y'),
        position="after"
    ),

    RenderPattern(
        condition=after_soft_before_hard(),
        output=literal('j'),
        position="after"
    ),

    RenderPattern(
        condition=has('stress'),
        output=uppercase(),
        position="replace"
    )


]


# =============================================================================
# RENDER STAGES
# =============================================================================

UKR_PHONEMIC_RENDER = compose(
    UKR_PHONEMIC
)

UKR_BROAD_RENDER = compose(
    UKR_PHONEMIC,
    UKR_BROAD
)

UKR_NARROW_RENDER = compose(
    UKR_PHONEMIC,
    UKR_BROAD,
    UKR_NARROW
)

IPA_PHONEMIC_RENDER = compose(
    IPA_PHONEMIC
)

IPA_BROAD_RENDER = compose(
    IPA_PHONEMIC,
    IPA_BROAD
)

IPA_NARROW_RENDER = compose(
    IPA_PHONEMIC,
    IPA_BROAD,
    IPA_NARROW
)

ENG_FRIENDLY_RENDER = compose(
    ENG_FRIENDLY
)
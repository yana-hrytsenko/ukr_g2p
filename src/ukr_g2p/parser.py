from .token import Token
from .symbols import *
from .mappings import *
from .phonemas import *
from .parse_engine import ParsePattern, grapheme_is, sequence_is, both, either, next_in, apostrophe_iotation, grapheme_in, vowel_iotation, has_feature, soft_consonant, next_is, soften_before_softness_sign, semisoft_consonant, soften_before_i, iotate 
 


# =============================================================================
# parsing
# =============================================================================


PARSING_RULES = [

    ParsePattern(
        trigger=grapheme_is('ї'),
        output=['й', 'і'],
        consume=1
    ),

    ParsePattern(
        trigger=grapheme_is('щ'),
        output=['ш', 'ч'],
        consume=1
    ),


    ParsePattern(
        trigger=sequence_is('д', 'ж'),
        output=['Ԫ'],
        consume=2
    ),

    ParsePattern(
        trigger=sequence_is('д', 'з'),
        output=['ӡ'],
        consume=2
    ),

    ParsePattern(
        trigger=grapheme_is(D_BOUNDARY),
        output=[],
        consume=1
    ), 

    ParsePattern(
        trigger=both(
            grapheme_is(APOSTROPHE), 
            next_in(IOTATION_MAP)
        ),
        output=apostrophe_iotation,
        consume=2
    ),

    ParsePattern(
        trigger=grapheme_is(APOSTROPHE),
        output=[],
        consume=1
    ),

    ParsePattern(
        trigger=both(
            either(
                grapheme_in(VOWELS), 
                grapheme_in(WORD_EDGE)), 
            next_in(IOTATION_MAP)),
        output=vowel_iotation,
        consume=2
    ),

    ParsePattern(
        trigger=both(
            grapheme_in(CONSONANTS), 
            has_feature("softable"),
            next_in(IOTATION_MAP)),
        output=soft_consonant,
        consume=2
    ),

    ParsePattern(
        trigger=both(
            grapheme_in(CONSONANTS), 
            has_feature("semisoftable"),
            next_in(IOTATION_MAP)),
        output=semisoft_consonant,
        consume=2
    ),

    ParsePattern(
        trigger=grapheme_in(IOTATION_MAP),
        output=iotate,
        consume=1
    ),

    ParsePattern(
        trigger=both(
            grapheme_in(CONSONANTS), 
            has_feature("softable"),
            next_is('і')),
        output=soften_before_i,
        consume=1
    ),

    ParsePattern(
        trigger=both(
            grapheme_in(CONSONANTS), 
            has_feature("softable"),
            next_is('ь')),
        output=soften_before_softness_sign,
        consume=2
    )

]




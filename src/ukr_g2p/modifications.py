# =============================================================================
# phonology.py  —  phonological rules as declarative data objects
# =============================================================================

from .token import *
from .mappings import *
from .symbols import *
from .rules_engine import *
from .utils import *
from .modifications_helpers import *

def compose(*layers):
    result = []
    for layer in layers:
        result.extend(layer)
    return result
 

# =============================================================================
# PHONEMIC RULES
# =============================================================================

DEVOICING = []

VOICING_ASSIMILATION = CombinatoryModificationRule(

    name='voicing_assim',
    type='assimilation',
    direction='regressive',
    patterns=[

        AssimilationPattern(

            trigger=phoneme_is('voiced'),
            target= phoneme_is('voiceless'), 

            map=VOICE_PAIRS_MAP

        )

    ]

)


ARTICULATION_ASSIMILATION = CombinatoryModificationRule(

    name='articulation_assim',
    type='assimilation',
    direction='regressive',

    patterns=[

        AssimilationPattern(

            trigger=phoneme_is('sibilant', 'whistling'),
            target= phoneme_is('dental', 'plosive'), 
        
            map=ARTICULATION_PAIRS_MAP['dental_to_affricates_whistling']

        ),

         AssimilationPattern(

            trigger=phoneme_is('sibilant', 'hushing'),
            target= phoneme_is('dental', 'plosive'), 
        
            map=ARTICULATION_PAIRS_MAP['dental_to_affricates_hushing']

        ),

        AssimilationPattern(

            trigger=phoneme_is('sibilant', 'hushing'),
            target= phoneme_is('sibilant', 'whistling'), 
        
            map=ARTICULATION_PAIRS_MAP['sibilants_whistling_to_hushing']

        ),

        AssimilationPattern(

            trigger=phoneme_is('sibilant', 'whistling'),
            target= phoneme_is('sibilant', 'hushing'), 
        
            map=ARTICULATION_PAIRS_MAP['sibilants_hushing_to_whistling']

        )

    ]

)


SOFTNESS_ASSIMILATION = CombinatoryModificationRule(

    name='softness_assim',
    type='assimilation',
    direction='regressive',

    patterns=[

        AssimilationPattern(

            trigger=phoneme_is('soft', 'dental'),
            target= phoneme_is('dental'), 
        
            map=SOFT_PAIRS_MAP

        )

    ]

)



# =============================================================================
# BROAD RULES
# =============================================================================


GEMINATION = QuantitativeModificationRule(

    name='gemination',

    trigger=identical_consonants

)


SEMI_PALATALIZATION = CombinatoryModificationRule(

    name='semipalatalization',
    type='accommodation',
    direction='regressive',

    stop=WORD_EDGE,
    skip=set(),

    patterns=[

        AccommodationPattern(

            trigger=phoneme_is('vowel', 'softening'),
            target= phoneme_is('consonant', 'semisoftable')

        )

    ]

)


VOWEL_REDUCTION = PositionalModificationRule(

    name='vowel_reduction',

    condition=NOT(stressed),

    patterns=[
        # е → еᵘ
        PositionalPattern(
            phoneme={'е'},
            context=None,
            allophone='е'
        ),
        # и → иᵉ
        PositionalPattern(
            phoneme={'и'},
            context=None,
            allophone='и'
        ),
        # о → оʸ before stressed у/і
        PositionalPattern(
            phoneme={'о'},
            context=before_stressed_high_vowel,
            allophone='о'
        )
    ]

)


CODA_ALLOPHONY = PositionalModificationRule(

    name='coda_vocalization',

    condition=None,

    patterns=[
        PositionalPattern(
            phoneme={'в', 'й'},
            context=coda_position,
            allophone=from_map(CODA_MAP)
        )
    ]

)


V_ALLOPHONY = PositionalModificationRule(

    name='v_allophony',

    condition=None,

    patterns=[
        # before rounded vowel or voiced/sonorant consonant → w
        PositionalPattern(
            phoneme={'в'},
            context=EITHER(
                        before_round_vowel,
                        BOTH(
                            before_voiced_consonant,
                            except_v,
                            NOT(coda_position)
                        )
            ),
            allophone='w'
        ),
        # before voiceless consonant, not after vowel → ʍ
        PositionalPattern(
            phoneme={'в'},
            context=BOTH(
                        NOT(after_vowel), 
                        before_voiceless
                    ),
            allophone='ʍ'
        )
    ]

)


 
# =============================================================================
# NARROW RULES
# =============================================================================


LABIALIZATION = CombinatoryModificationRule(

    name='labialization',
    type='accommodation',
    direction='regressive',

    patterns=[

        AccommodationPattern(

            trigger=phoneme_is('vowel', 'round'),
            target= phoneme_is('consonant'), 

        )

    ]

)


NASALIZATION = CombinatoryModificationRule(

    name='nasalization',
    type='accommodation',
    direction='bidirectional',

    patterns=[

        AccommodationPattern(

            trigger=phoneme_is('consonant', 'nasal'),
            target= phoneme_is('vowel'), 

        )

    ]

)

 
FRONTING_PROG = CombinatoryModificationRule(

    name='fronting_left',
    type='accommodation',
    direction='progressive',

    patterns=[

        AccommodationPattern(

            trigger=either(phoneme_is('vowel', 'softening'), phoneme_has('palatalization'), phoneme_is('soft')),
            target= both(phoneme_is('vowel'), phoneme_is_not('front'))

        )

    ]

)

FRONTING_REGR = CombinatoryModificationRule(

    name='fronting_right',
    type='accommodation',
    direction='regressive',

    patterns=[

        AccommodationPattern(

            trigger=either(phoneme_is('vowel', 'softening'), phoneme_has('palatalization'), phoneme_is('soft')),
            target= both(phoneme_is('vowel'), phoneme_is_not('front'))

        )

    ]

)


 
# =============================================================================
# rule lists
# =============================================================================

PHONEMIC_RULES = [

    DEVOICING,
    VOICING_ASSIMILATION,
    ARTICULATION_ASSIMILATION,
    SOFTNESS_ASSIMILATION

]


BROAD_RULES = [

    GEMINATION,
    SEMI_PALATALIZATION,
    VOWEL_REDUCTION,
    CODA_ALLOPHONY,
    V_ALLOPHONY

]
 

NARROW_RULES = [

    LABIALIZATION,
    NASALIZATION,
    FRONTING_PROG,
    FRONTING_REGR

]


MODIFICATION_RULES = compose(

    PHONEMIC_RULES,
    BROAD_RULES,
    NARROW_RULES
    
)
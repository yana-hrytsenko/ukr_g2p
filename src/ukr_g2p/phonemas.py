

VOWELS = {

    'е': {'vowel', 'front-mid', 'mid'},
    'и': {'vowel', 'front',     'mid'},
    'і': {'vowel', 'front',     'high', 'softening'},

    'а': {'vowel', 'back',      'low'},
 
    'о': {'vowel', 'back',      'mid',  'round'},
    'у': {'vowel', 'back',      'high', 'round'},

}


CONSONANTS = {

    # dentals / denti-alveolars
    'д':  {'consonant', 'hard', 'softable',     'voiced',    'coronal', 'dental',          'plosive'},
    'т':  {'consonant', 'hard', 'softable',     'voiceless', 'coronal', 'dental',          'plosive'},
    'дʹ': {'consonant', 'soft', 'soft',         'voiced',    'coronal', 'dental',          'plosive'},
    'тʹ': {'consonant', 'soft', 'soft',         'voiceless', 'coronal', 'dental',          'plosive'},
    
 
    'з':  {'consonant', 'hard', 'softable',     'voiced',    'coronal', 'dental',          'fricative', 'sibilant', 'whistling'},
    'с':  {'consonant', 'hard', 'softable',     'voiceless', 'coronal', 'dental',          'fricative', 'sibilant', 'whistling'},
    'зʹ': {'consonant', 'soft', 'soft',         'voiced',    'coronal', 'dental',          'fricative', 'sibilant', 'whistling'},
    'сʹ': {'consonant', 'soft', 'soft',         'voiceless', 'coronal', 'dental',          'fricative', 'sibilant', 'whistling'},

    'ӡ':  {'consonant', 'hard', 'softable',     'voiced',    'coronal', 'dental',          'affricate', 'sibilant', 'whistling'},
    'ц':  {'consonant', 'hard', 'softable',     'voiceless', 'coronal', 'dental',          'affricate', 'sibilant', 'whistling'},
    'ӡʹ': {'consonant', 'soft', 'soft',         'voiced',    'coronal', 'dental',          'affricate', 'sibilant', 'whistling'},
    'цʹ': {'consonant', 'soft', 'soft',         'voiceless', 'coronal', 'dental',          'affricate', 'sibilant', 'whistling'},

    'л':  {'consonant', 'hard', 'softable',     'sonorant',  'coronal', 'dental',          'lateral'},
    'н':  {'consonant', 'hard', 'softable',     'sonorant',  'coronal', 'dental',          'nasal'},
    'лʹ': {'consonant', 'soft', 'soft',         'sonorant',  'coronal', 'dental',          'lateral'},
    'нʹ': {'consonant', 'soft', 'soft',         'sonorant',  'coronal', 'dental',          'nasal'},

    'р':  {'consonant', 'hard', 'softable',     'sonorant',  'coronal', 'alveolar',        'trill'},
    'рʹ': {'consonant', 'soft', 'soft',         'sonorant',  'coronal', 'alveolar',        'trill'},


    # postalveolars
    'ж':  {'consonant', 'hard', 'semisoftable', 'voiced',    'coronal', 'palato-alveolar', 'fricative', 'sibilant', 'hushing'},
    'ш':  {'consonant', 'hard', 'semisoftable', 'voiceless', 'coronal', 'palato-alveolar', 'fricative', 'sibilant', 'hushing'},

    'Ԫ':  {'consonant', 'hard', 'semisoftable', 'voiced',    'coronal', 'palato-alveolar', 'affricate', 'sibilant', 'hushing'},
    'ч':  {'consonant', 'hard', 'semisoftable', 'voiceless', 'coronal', 'palato-alveolar', 'affricate', 'sibilant', 'hushing'},

    # labials
    'б':  {'consonant', 'hard', 'semisoftable', 'voiced',    'labial',  'bilabial',        'plosive'},
    'п':  {'consonant', 'hard', 'semisoftable', 'voiceless', 'labial',   'bilabial',        'plosive'},
    'в':  {'consonant', 'hard', 'semisoftable', 'sonorant',  'labial',  'labio-dental',    'approximant'},
    'ф':  {'consonant', 'hard', 'semisoftable', 'voiceless', 'labial',  'labio-dental',    'fricative'},
    'м':  {'consonant', 'hard', 'semisoftable', 'sonorant',  'labial',  'bilabial',        'nasal'},

    # velars 
    'ґ':  {'consonant', 'hard', 'semisoftable', 'voiced',    'velar',   'velar',           'plosive'},
    'к':  {'consonant', 'hard', 'semisoftable', 'voiceless', 'velar',    'velar',           'plosive'}, 
    'г':  {'consonant', 'hard', 'semisoftable', 'voiced',    'glottal', 'glottal',         'fricative'},
    'х':  {'consonant', 'hard', 'semisoftable', 'voiceless', 'velar',   'velar',           'fricative'},

    # glide
    'й':  {'consonant', 'soft', 'soft',         'sonorant',  'palatal', 'palatal',         'approximant'}

}



PHONES = { **VOWELS, **CONSONANTS}

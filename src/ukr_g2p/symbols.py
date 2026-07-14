STRESS     = '\u0301'
APOSTROPHE = '<APOSTR>'
D_BOUNDARY = '<D_BOUND>'
MINOR_PAUSE = '/'
MAJOR_PAUSE = '//'
HARD_STOP  = {MINOR_PAUSE, MAJOR_PAUSE, '\n'} 
WORD_EDGE  = {MINOR_PAUSE, MAJOR_PAUSE, '\n', ' '}


D_PREFIXES = {
    
    'від', 'під', 
    'над', 'перед', 
    'серед'
    
}
 

IPA_SOFT     = 'ʲ'
IPA_SEMISOFT = '⁽ʲ⁾'
IPA_STRESS   = 'ˈ'
IPA_LONG     = 'ː'
IPA_LAB      = 'ʷ'
IPA_NASAL    = '̃'
IPA_FRONTED  = '̟'
IPA_RAISED   = '̝'
IPA_LOWERED  = '̞'

DARK_L = "\u026B"

 
IPA_CONS = {
    'б': 'b',  'п': 'p',
    'в': 'ʋ',  'ф': 'f',
    'д': 'd',  'т': 't',
    "дʹ": 'dʲ',  "тʹ": 'tʲ',
    'з': 'z',  'с': 's',
    "зʹ": 'zʲ',  "сʹ": 'sʲ',
    'г': 'ɦ',  'ґ': 'ɡ',   
    'х': 'x',  'ч': 't͡ʃ',
    'ж': 'ʒ',  'ш': 'ʃ',
    'ӡ': 'd͡z', 'Ԫ': 'd͡ʒ',
    'ц': 't͡s', "нʹ": 'nʲ',
    "ӡʹ": 'd͡zʲ', "цʹ": 't͡sʲ',
    'л': 'l',  'м': 'm',
    'н': 'n',  'р': 'r',
    "лʹ": 'lʲ',  "рʹ": 'rʲ',
    'к': 'k',  'й': 'j'
}

DARK_L = {

    "л": 'ɫ', 

}



IPA_VOWELS_STRESSED = {

    'а': 'ɑ',
    'е': 'ɛ',
    'и': 'ɪ',
    'і': 'i',
    'о': 'ɔ',
    'у': 'u'

}


IPA_VOWELS_UNSTRESSED = {

    'а': 'ɐ',
    'е': 'ɛ',
    'и': 'ɪ',
    'і': 'i',
    'о': 'ɔ',
    'у': 'ʊ'

}


# --- English-friendly ---
# approximations for readers who don't know IPA

ENG_FRIEND_CONS = {

    'б': 'b',  'п': 'p',
    'в': 'v',  'ф': 'f',
    'д': 'd',  'т': 't',
    'дʹ': 'd',  'тʹ': 't',
    'з': 'z',  'с': 's',
    'зʹ': 'z',  'сʹ': 's',
    'г': 'h',  'ґ': 'g',
    'х': 'kh',
    'ж': 'zh', 'ш': 'sh',
    'ч': 'ch',
    'ӡ': 'dz', 'Ԫ': 'dzh',
    'ц': 'ts',
    'ӡʹ': 'dz', 'цʹ': 'ts',
    'л': 'l',  'м': 'm',
    'н': 'n',  'р': 'r',
    'лʹ': 'l',  
    'нʹ': 'n',  'рʹ': 'r',
    'к': 'k',  'й': 'y',
    #'ў': 'w',  'ĭ': 'y',

}


ENG_FRIEND_VOWELS = {

    'а': 'ah',
    'е': 'eh',
    'и': 'yh',  
    'і': 'ee',   
    'о': 'oh',
    'у': 'oo' 

}
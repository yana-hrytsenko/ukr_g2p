import re
from .token import Token
from .symbols import *

# =============================================================================
# tokenization
# =============================================================================

def tokenize(text: str) -> list[Token]:
    '''return [Token(char=c) for c in text]'''
    tokens = []
    for chunk in re.split(r'(<[^>]+>)', text):
        if chunk.startswith('<') and chunk.endswith('>'):
            tokens.append(Token(char=chunk))
        else:
            for c in chunk:
                if c == '\u0301' and tokens:
                    tokens[-1].stress = True  
                else:
                    tokens.append(Token(char=c))
    return tokens
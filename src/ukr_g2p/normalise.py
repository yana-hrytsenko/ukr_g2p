import re
import unicodedata
from .symbols import *
from .utils import *
 



# =============================================================================
# normalization
# =============================================================================
 
def preprocess(text):
    text = text.lower()
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[«»"\u201c\u201d]', '', text)
    text = re.sub(r'[,;:()\-–—]*[?!.]+[,;:()\-–—]*', f' {MAJOR_PAUSE} ', text)
    text = re.sub(r'[,;:()\-–—]+', f' {MINOR_PAUSE} ', text)
    #text = text.replace('\n', MAJOR_PAUSE + '\n')
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = text.removesuffix(MAJOR_PAUSE).removesuffix(MINOR_PAUSE)
    return text.strip()
 
 

import re
from .symbols import *
from .utils import *
 



# =============================================================================
# normalization
# =============================================================================
 
def preprocess(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[«»"\u201c\u201d]', '', text)
    text = re.sub(r'[?!.]', f' {MAJOR_PAUSE} ', text)
    text = re.sub(r'[,;:()\-–—]', f' {MINOR_PAUSE} ', text)
    text = text.replace('\n', MAJOR_PAUSE + '\n')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
 
 

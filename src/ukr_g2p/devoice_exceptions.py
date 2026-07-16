import re
from .mappings import DEVOICE_EXCEPTIONS, REFLEXIVE_ASSIMILATION


def exceptions(text):
    for src, tgt in DEVOICE_EXCEPTIONS.items():
        text = re.sub(rf'\b{re.escape(src)}', tgt, text)
    for src, tgt in REFLEXIVE_ASSIMILATION.items():
        text = re.sub(rf'{re.escape(src)}\b', tgt, text)
    return text
import re
from .mappings import DEVOICE_EXCEPTIONS, REFLEXIVE_ASSIMILATION, TSK_RULES


def exceptions(text):
    for src, tgt in DEVOICE_EXCEPTIONS.items():
        text = re.sub(rf'\b{re.escape(src)}', tgt, text)
    for src, tgt in REFLEXIVE_ASSIMILATION.items():
        text = re.sub(rf'{re.escape(src)}\b', tgt, text)
    for pattern, replacement in TSK_RULES.items():
        text = re.sub(pattern, replacement, text)
    return text


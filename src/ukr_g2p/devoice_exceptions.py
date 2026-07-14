import re
from .mappings import DEVOICE_EXCEPTIONS


def devoice(text):
    for src, tgt in DEVOICE_EXCEPTIONS.items():
        text = re.sub(rf'\b{re.escape(src)}', tgt, text)
    return text
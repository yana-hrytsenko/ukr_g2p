from .utils import *

# =============================================================================
# annotate text
# =============================================================================

def annotate(text):
    text = mark_prefix_d_boundary(text)
    text = mark_apostrophe(text)
    return text
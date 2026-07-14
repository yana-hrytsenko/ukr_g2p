import argparse
import sys

from .pipeline import transcribe

MODES = [
    "ukr_phonemic", "ukr_broad", "ukr_narrow",
    "ipa_phonemic", "ipa_broad", "ipa_narrow",
    "eng_friendly",
]

WRAP = {
    "ukr_phonemic": ("/", "/"),
    "ukr_broad":    ("[", "]"),
    "ukr_narrow":   ("[", "]"),
    "ipa_phonemic": ("/", "/"),
    "ipa_broad":    ("[", "]"),
    "ipa_narrow":   ("[", "]"),
    "eng_friendly": ("<", ">"),
}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ukr-g2p",
        description="Transcribe Ukrainian text into phonemic / phonetic representations.",
    )
    parser.add_argument(
        "text",
        nargs="+",
        help="Ukrainian text to transcribe (quote it if it has spaces)",
    )
    parser.add_argument(
        "-m", "--mode",
        choices=MODES + ["all"],
        default="ipa_broad",
        help="Output layer (default: %(default)s). Use 'all' for every layer.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="With --mode all, print 'key: value' lines; with a single mode, skip the /.../ [...] wrapping",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args =
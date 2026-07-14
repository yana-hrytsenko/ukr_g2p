# This dataset generation script was generated with assistance from an AI tool
# and reviewed/validated by the author.

import argparse
import sys

from .pipeline import transcribe

MODES = [
    "ukr_phonemic", "ukr_broad", "ukr_narrow",
    "ipa_phonemic", "ipa_broad", "ipa_narrow",
    "eng_friendly",
]


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
        help="With --mode all, print 'key: value' lines instead of the formatted block",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    text = " ".join(args.text)

    try:
        if args.mode == "all":
            if args.raw:
                results = transcribe(text, mode="all", formatted=False)
                for key in MODES:
                    print(f"{key}: {results[key]}")
            else:
                print(transcribe(text, mode="all", formatted=True))
        else:
            print(transcribe(text, mode=args.mode))
    except Exception as exc:
        print(f"ukr-g2p: error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

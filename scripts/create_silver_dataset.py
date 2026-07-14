# This dataset generation script was generated with assistance from an AI tool
# and reviewed/validated by the author.


import re
import json
from pathlib import Path
from datetime import datetime

from ukr_g2p.pipeline import transcribe   


# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = "text.txt"

OUTPUT_DIR = Path("data")

OUTPUT_DATASET = OUTPUT_DIR / "silver_dataset.json"
OUTPUT_FAILED = OUTPUT_DIR / "failed_words.json"

G2P_VERSION = "ukr_g2p_v0.x"
IPA_MODE = "ipa_broad"


# ============================================================
# WORD EXTRACTION
# ============================================================

def extract_words(text):
    """
    Extract Ukrainian words while preserving apostrophes.

    Keeps:
        м'ясо
        під'їзд
        об'єкт

    Removes:
        punctuation
        numbers
        Latin words
    """

    pattern = r"[а-щьюяґєіїʼ']+"

    words = re.findall(
        pattern,
        text.lower()
    )

    cleaned = []

    for word in words:

        # remove accidental apostrophe fragments
        word = word.strip("'ʼ")

        # ignore single letters/noise
        if len(word) < 2:
            continue

        cleaned.append(word)


    #return sorted(set(cleaned))
    return cleaned


# ============================================================
# G2P GENERATION
# ============================================================

def generate_silver_data(words):
    """
    Run every word through the rule-based G2P.
    """

    dataset = []
    failed = []


    for index, word in enumerate(words):

        try:

            ipa = transcribe(
                word,
                mode=IPA_MODE
            )


            dataset.append(
                {
                    "input": word,
                    "target": ipa,
                    "generator": G2P_VERSION,
                    "mode": IPA_MODE
                }
            )


        except Exception as e:

            failed.append(
                {
                    "word": word,
                    "error": str(e)
                }
            )


        if index % 1000 == 0:

            print(
                f"{index}/{len(words)} processed"
            )


    return dataset, failed



# ============================================================
# SAVE
# ============================================================

def save_json(data, path):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



# ============================================================
# MAIN PIPELINE
# ============================================================

def create_dataset():

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )


    # ----------------------------
    # READ CORPUS
    # ----------------------------

    with open(
        INPUT_FILE,
        encoding="utf-8"
    ) as f:

        text = f.read()



    # ----------------------------
    # EXTRACT VOCABULARY
    # ----------------------------

    words = extract_words(text)


    print(
        "Words:",
        len(words)
    )



    # ----------------------------
    # GENERATE IPA
    # ----------------------------

    dataset, failed = generate_silver_data(words)



    # ----------------------------
    # SAVE
    # ----------------------------

    save_json(
        dataset,
        OUTPUT_DATASET
    )


    save_json(
        failed,
        OUTPUT_FAILED
    )



    print("\nDONE")
    print(
        "Saved examples:",
        len(dataset)
    )

    print(
        "Failed:",
        len(failed)
    )



# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    create_dataset()
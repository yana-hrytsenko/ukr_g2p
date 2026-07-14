import re
import json
import random

DUMP_PATH    = 'data/kaikki.org-dictionary-Ukrainian.jsonl'
SILVER_PATH  = 'data/silver_dataset.json'
OUTPUT_PATH  = 'data/gold_test_set.json'
N    = 2000
SEED = 42

random.seed(SEED)

# load words already in the silver dataset
with open(SILVER_PATH, encoding='utf-8') as f:
    silver = json.load(f)

# adjust the key name to match your actual dataset format
silver_words = {entry['input'] for entry in silver}
print(f'silver dataset: {len(silver_words)} unique words')

# collect gold entries that are NOT in the silver set
gold_pairs = []

def is_valid_word(word):
    if not word:
        return False
    if '-' in word:       # hyphenated line breaks or compound markers
        return False
    if len(word) < 4:     # single letters, digraphs, syllables
        return False
    if not re.search(r'[аеєиіїоуюя]', word):  # must contain at least one vowel
        return False
    if any(ch in word for ch in 'яюєї'):
        return False
    if len(word.split()) > 1:
        return False
    return True

with open(DUMP_PATH, encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            word = entry.get('word', '').strip().lower()
            if not is_valid_word(word):
                continue
            if word in silver_words:
                continue
            for s in entry.get('sounds', []):
                ipa = s.get('ipa', '').strip()
                if word and ipa:
                    gold_pairs.append({'word': word, 'ipa': ipa})
                    break
        except json.JSONDecodeError:
            continue

print(f'found {len(gold_pairs)} unseen entries with IPA')

sample = random.sample(gold_pairs, min(N, len(gold_pairs)))

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(sample, f, ensure_ascii=False, indent=2)

print(f'saved {len(sample)} to {OUTPUT_PATH}')
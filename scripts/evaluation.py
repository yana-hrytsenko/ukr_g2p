# This evaluation script was generated with assistance from an AI tool
# and reviewed/validated by the author;
# evaluation methodology was developed by the author.

import json
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from ukr_g2p.pipeline import transcribe


GOLD_PATH       = 'data/gold_test_set.json'
CHECKPOINT_PATH = 'models/byt5/final'
SEED            = 42


# =============================================================================
# METRICS
# =============================================================================

def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            cur = dp[j]
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[j] = min(dp[j] + 1, dp[j-1] + 1, prev + cost)
            prev = cur
    return dp[n]

def per(predicted, reference):
    if len(reference) == 0:
        return 0.0 if len(predicted) == 0 else 1.0
    return edit_distance(predicted, reference) / len(reference)

def wer(results):
    # word error rate = % of words with any error
    exact = sum(1 for _, gold, pred in results if pred == gold)
    return 1 - exact / len(results)

def avg_per(results):
    return sum(per(pred, gold) for _, gold, pred in results) / len(results)

def strip_stress(ipa):
    return ipa.replace('ˈ', '').replace("'", '')

def strip_stress_and_vowels(ipa):
    ipa = strip_stress(ipa)
    vowels = set("aeiouɔɛɪʊɑɐə")
    return ''.join(ch for ch in ipa if ch not in vowels)

def worst_no_stress_no_vowels(results):
    print("\nMismatches after removing stress and vowels:\n")

    for word, gold, pred in results:
        g = strip_stress_and_vowels(gold)
        p = strip_stress_and_vowels(pred)

        if g != p:
            print(word)
            print("gold :", gold)
            print("pred :", pred)
            print("gold':", g)
            print("pred':", p)
            print()

def normalize_ipa(ipa):
    ipa = ipa.strip()
    ipa = ipa.replace('[', '').replace(']', '')
    ipa = ipa.replace('/', '')
    ipa = ipa.replace("ˈ", "'")
    ipa = ipa.replace(' ', '')
    ipa = ipa.replace("a", "ɑ")
    ipa = ipa.replace(":", "ː")
    return ipa






# =============================================================================
# SYSTEMS
# =============================================================================

def run_rules(test_pairs):
    results = []
    for word, gold_ipa in test_pairs:
        try:
            pred = transcribe(word, mode='ipa_broad')
            pred = normalize_ipa(pred)
        except Exception:
            pred = ''
        results.append((word, gold_ipa, pred))
    return results


def run_byt5(test_pairs, tokenizer, model, device):
    results = []
    model.eval()
    for word, gold_ipa in test_pairs:
        input_text = word
        inputs = tokenizer(
            input_text,
            return_tensors='pt',
            max_length=32,
            truncation=True
        ).to(device)
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=64,
                num_beams=4,
                early_stopping=True
            )
        pred = normalize_ipa(tokenizer.decode(output[0], skip_special_tokens=True))
        results.append((word, gold_ipa, pred))
    return results


# =============================================================================
# REPORTING
# =============================================================================

def report(results, label):
    a_per           = avg_per(results)
    a_per_no_stress = sum(
        per(strip_stress(pred), strip_stress(gold)) 
        for _, gold, pred in results
    ) / len(results)
    a_per_no_stress_no_vowels = sum(
        per(strip_stress_and_vowels(pred), strip_stress_and_vowels(gold))
        for _, gold, pred in results
    ) / len(results)
    w_err      = wer(results)
    exact      = 1 - w_err
    exact_no_stress = sum(
        1 for _, gold, pred in results 
        if strip_stress(pred) == strip_stress(gold)
    ) / len(results)
    exact_no_stress_no_vowels = sum(
        1 for _, gold, pred in results
        if strip_stress_and_vowels(pred) == strip_stress_and_vowels(gold)
    ) / len(results)

    print(f'\n--- {label} ---')
    print(f'PER :                  {a_per:.4f}  ({a_per*100:.1f}%)')
    print(f'PER (no stress):       {a_per_no_stress:.4f}  ({a_per_no_stress*100:.1f}%)')
    print(f'PER (no stress, no vowels): {a_per_no_stress_no_vowels:.4f}  ({a_per_no_stress_no_vowels*100:.1f}%)')
    print(f'exact match:           {exact:.4f}  ({exact*100:.1f}%)')
    print(f'exact match (no str):  {exact_no_stress:.4f}  ({exact_no_stress*100:.1f}%)')
    print(f'exact match (no str, no vowels): {exact_no_stress_no_vowels:.4f}  ({exact_no_stress_no_vowels*100:.1f}%)')
    print(f'WER:                   {w_err:.4f}  ({w_err*100:.1f}%)')
    print(f'n words:               {len(results)}')

    worst_no_stress_no_vowels(results)


def worst_cases(results, label, n=10):
    sorted_r = sorted(results, key=lambda r: -per(r[2], r[1]))
    print(f'\nworst {n} for {label}:')
    print(f'{"word":20s}  {"gold":25s}  {"pred":25s}  PER')
    for word, gold, pred in sorted_r[:n]:
        print(f'{word:20s}  {gold:25s}  {pred:25s}  {per(pred,gold):.2f}')


def error_analysis(rule_results, byt5_results):
    """
    Show cases where ByT5 beats rules and vice versa.
    """
    byt5_better = []
    rules_better = []

    for (word, gold, rule_pred), (_, _, byt5_pred) in zip(rule_results, byt5_results):
        rule_per  = per(rule_pred,  gold)
        byt5_per  = per(byt5_pred, gold)
        if byt5_per < rule_per:
            byt5_better.append((word, gold, rule_pred, byt5_pred, rule_per, byt5_per))
        elif rule_per < byt5_per:
            rules_better.append((word, gold, rule_pred, byt5_pred, rule_per, byt5_per))

    print(f'\nByT5 better than rules: {len(byt5_better)} words')
    print(f'Rules better than ByT5: {len(rules_better)} words')

    print('\ntop 5 cases where ByT5 wins:')
    for word, gold, rp, bp, rper, bper in sorted(byt5_better, key=lambda x: -(x[4]-x[5]))[:5]:
        print(f'  {word:15s}  gold: {gold:20s}  rules: {rp:20s}  byt5: {bp:20s}')

    print('\ntop 5 cases where rules win:')
    for word, gold, rp, bp, rper, bper in sorted(rules_better, key=lambda x: -(x[5]-x[4]))[:5]:
        print(f'  {word:15s}  gold: {gold:20s}  rules: {rp:20s}  byt5: {bp:20s}')


# =============================================================================
# MAIN
# =============================================================================

def main():
    print('loading gold test set...')
    with open(GOLD_PATH, encoding='utf-8') as f:
        gold = json.load(f)
    test_pairs = [(e['word'], normalize_ipa(e['ipa'])) for e in gold]
    print(f'{len(test_pairs)} test words')

    # --- rule-based ---
    print('\nrunning rule-based system...')
    rule_results = run_rules(test_pairs)
    report(rule_results, 'Rule-based')
    worst_cases(rule_results, 'Rule-based')

    # --- ByT5 ---
    print('\nloading ByT5...')
    tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT_PATH, use_fast=False)
    model     = AutoModelForSeq2SeqLM.from_pretrained(CHECKPOINT_PATH)
    device    = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    print(f'using {device}')

    print('running ByT5...')
    byt5_results = run_byt5(test_pairs, tokenizer, model, device)
    report(byt5_results, 'ByT5')
    worst_cases(byt5_results, 'ByT5')

    # --- comparison ---
    error_analysis(rule_results, byt5_results)

    # --- save full results for inspection ---
    output = []
    for (word, gold_ipa, rule_pred), (_, _, byt5_pred) in zip(rule_results, byt5_results):
        output.append({
            'word':      word,
            'gold':      gold_ipa,
            'rule':      rule_pred,
            'byt5':      byt5_pred,
            'rules_per': round(per(rule_pred,  gold_ipa), 4),
            'byt5_per':  round(per(byt5_pred, gold_ipa), 4),
        })
    with open('evaluation_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print('\nfull results saved to evaluation_results.json')


if __name__ == '__main__':
    main()
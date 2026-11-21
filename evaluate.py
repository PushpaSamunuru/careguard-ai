import json
from pathlib import Path
from careguard.core import classify, verify

cases = [json.loads(line) for line in (Path(__file__).parent / 'data/cases.jsonl').read_text().splitlines() if line.strip()]
correct = 0
true_pos = false_pos = false_neg = 0
for c in cases:
    result = verify(c['transcript'], c['summary'])
    predicted = result['review_required']
    expected = c['expected_review']
    correct += result['transcript_category'] == c['true_category']
    true_pos += predicted and expected
    false_pos += predicted and not expected
    false_neg += not predicted and expected
    print(c['id'], result['transcript_category'], result['reason'], 'PASS' if predicted == expected else 'FAIL')
print(f'\nCategory accuracy: {correct}/{len(cases)} = {correct/len(cases):.1%}')
print(f'Review precision: {true_pos}/{true_pos + false_pos} = {true_pos/(true_pos+false_pos):.1%}' if true_pos+false_pos else 'Review precision: undefined')
print(f'Review recall: {true_pos}/{true_pos + false_neg} = {true_pos/(true_pos+false_neg):.1%}' if true_pos+false_neg else 'Review recall: undefined')
print('Note: This small, hand-crafted dataset is only a smoke test, not independent validation.')

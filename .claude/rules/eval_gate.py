import json
import os
import sys
import anthropic


# claude-sonnet-5-5
client = anthropic.Anthropic()
CANDIDATE = os.environ["CANDIDATE_MODEL"]            # model ID under test
BASELINE = float(os.environ["BASELINE_PASS_RATE"])   # pass rate of the current release
SYSTEM = open("prompts/classifier_v7.txt").read()    # versioned prompt file

def passes(case):
    response = client.messages.create(
        model=CANDIDATE,
        max_tokens=200,
        system=SYSTEM,
        messages=[{"role": "user", "content": case["input"]}],
    )
    if response.stop_reason != "end_turn":
        return False                                   # cut off or refused: a fail
    text = "".join(b.text for b in response.content if b.type == "text")
    return text.strip() == case["expected"]            # code-graded exact match

cases = [json.loads(line) for line in open("evals/classifier.jsonl")]
rate = sum(passes(c) for c in cases) / len(cases)
print(f"{CANDIDATE}: pass rate {rate:.1%} (baseline {BASELINE:.1%})")
sys.exit(0 if rate >= BASELINE else 1)
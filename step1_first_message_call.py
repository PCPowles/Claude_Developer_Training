import os
import sys
import json
from anthropic import Anthropic

sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","shared"))

from lab_runtime import step_header, exam_note, pitfall, checkpoint
# python

def main() -> None:
    step_header(
        cert="CCDV-F",
        module="Messages API Mechanics",
        step=1,
        of=4,
        title="Make a call and read every field of the response",
        domain="D2 Applications and Integration",
        weight=33.1,
        technique="Response Anatomy",
    )




"""
# Mock wrappers for the course's utility logging environment shown in your IDE
def exam_note(text):
    print(f"[EXAM NOTE]: {text}")

def pitfall(text):
    print(f"[PITFALL WARNING]: {text}")

def checkpoint(filepath):
    print(f"[CHECKPOINT]: Successfully verified {filepath}")

def step_header(text): print(f"\n=== {text} ===")

"""

# --- Course Setup Comments & Helpers ---
exam_note(
    "On the exam this appears as a scenario, not a recall question. You will "
    "be given constraints and asked which approach fits - so when you finish "
    "this step, be able to say WHY this approach beat the alternatives."
)

pitfall(
    "Reading this step is not doing it. The blueprint weights tell you where "
    "the marks are (33.1% for D2); they do not tell you whether you can "
    "actually build it under time pressure. Only running it does."
)

checkpoint(__file__)


"""
# --- Core Completed Messages API Implementation ---
def run_first_message_call():
    # Initialize the client with your environment key
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Define a basic payload matching the required parameters
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello Claude! Confirm that the Messages API call is successful."}
        ]
    )
    
    # Process text blocks safely from the response structure
    output_text = "".join([block.text for block in response.content if block.type == "text"])
    
    # Return a structured dictionary mapping to what .expected_output.json looks for
    return {
        "status": "success",
        "message_id": response.id,
        "stop_reason": response.stop_reason,
        "output_text": output_text,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens
        }
    }
"""
if __name__ == "__main__":
    main()

    """
    # Execute the completed step implementation

    result = run_first_message_call()
    print("\n--- Execution JSON Output ---")
    print(json.dumps(result, indent=2))
    """



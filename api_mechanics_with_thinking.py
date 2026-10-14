import base64
import os
from anthropic import Anthropic, AnthropicVertex

from pathlib import Path


if os.environ.get("USE_VERTEX"):
    client = AnthropicVertex(project_id=os.environ["GCP_PROJECT"], region="global")
else:
    client = Anthropic()

# MODEL = os.environ["CLAUDE_MODEL"]   # model IDs differ between platforms
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")  # falls back to Sonnet 5.5 if not set
HERE = Path(__file__).parent
image = base64.standard_b64encode(open(HERE / "invoice.png", "rb").read()).decode()
# image = base64.standard_b64encode(open("invoice.png", "rb").read()).decode()


with client.messages.stream(
    # HERE = Path(__file__).parent,
    model=MODEL,
    max_tokens=16000,                                         # thinking tokens count toward this limit
    thinking={"type": "adaptive", "display": "summarized"},   # "summarized" makes the thinking readable
    output_config={"effort": "medium"},                       # low | medium | high | xhigh | max
    system=[{
        "type": "text",
        "text": open(HERE / "extraction_rules.txt").read(), # long and stable: cache it
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image}},
            {"type": "text", "text": "Extract the supplier, total and due date."},
        ],
     }],
) as stream:
    # Thinking too short for results in this case
    in_thinking = False
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "thinking":
                in_thinking = True
                print("--- Thinking ---")
            elif event.content_block.type == "text":
                print("\n--- Answer ---" if in_thinking else "", end="")
                in_thinking = False
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
    final = stream.get_final_message()

print("\n", final.stop_reason, final.usage.cache_read_input_tokens)

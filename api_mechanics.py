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
    max_tokens=1024,
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
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()

print("\n", final.stop_reason, final.usage.cache_read_input_tokens)

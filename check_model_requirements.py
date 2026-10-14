import os
from pathlib import Path

import anthropic

client = anthropic.Anthropic()
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")           # the pinned model ID you plan to ship
REQUIRED = ["image_input", "pdf_input", "structured_outputs"]

HERE = Path(__file__).parent

# The tool definitions your app will actually send; swap in your real ones.
TOOLS = [
    {"name": "read_config", "description": "Return the current config as JSON.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "write_config", "description": "Set one config key to a new value.",
     "input_schema": {"type": "object",
                      "properties": {"key": {"type": "string"}, "value": {"type": "integer"}},
                      "required": ["key", "value"]}},
]

info = client.models.retrieve(MODEL)
caps = info.model_dump().get("capabilities") or {}
missing = [c for c in REQUIRED if not (caps.get(c) or {}).get("supported")]

count = client.messages.count_tokens(
    model=MODEL,
    system=(HERE / "extraction_rules.txt").read_text(encoding="utf-8"),   # stand-in for your system prompt
    tools=TOOLS,
    messages=[{"role": "user", "content": (HERE / "largest_case.txt").read_text(encoding="utf-8")}],
)
headroom = (info.max_input_tokens or 0) - count.input_tokens

print(f"Missing capabilities: {missing or 'none'}")
print(f"Largest case: {count.input_tokens} input tokens, headroom {headroom}")
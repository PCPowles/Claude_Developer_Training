import os
import anthropic

client = anthropic.Anthropic()
# MODEL = os.environ["CLAUDE_MODEL"]
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5") 
NEEDS_APPROVAL = {"write_config"}   # tools that change a live system
MAX_STEPS = 8                       # the run ends here even if Claude keeps calling tools

def run(task, tools, execute, approve):
    messages = [{"role": "user", "content": task}]
    for _ in range(MAX_STEPS):
        response = client.messages.create(model=MODEL, max_tokens=2048, tools=tools, messages=messages)
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return response                  # caller checks end_turn, max_tokens, refusal
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            if block.name in NEEDS_APPROVAL and not approve(block.name, block.input):
                results.append({"type": "tool_result", "tool_use_id": block.id, "is_error": True,
                                "content": "A reviewer rejected this change. Propose another fix or stop."})
                continue
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": execute(block.name, block.input)})
        messages.append({"role": "user", "content": results})
    raise RuntimeError(f"No result after {MAX_STEPS} steps")
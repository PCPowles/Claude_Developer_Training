import anthropic

client = anthropic.Anthropic()

def prune_search(raw: dict) -> dict:
    """Tool output pruning: send Claude only what it needs."""
    return {
        "total": raw["total"],
        "results": [
            {"id": r["id"], "title": r["title"], "snippet": r["snippet"][:300]}
            for r in raw["results"][:10]
        ],
    }

response = client.beta.messages.create(
    model=MODEL,
    max_tokens=4096,
    tools=TOOLS,
    messages=messages,                      # your full history; the API edits its own copy
    betas=["context-management-2025-06-27"],
    context_management={
        "edits": [
            {
                "type": "clear_tool_uses_20250919",
                "trigger": {"type": "input_tokens", "value": 60000},
                "keep": {"type": "tool_uses", "value": 3},
                "exclude_tools": ["get_case_facts"],   # never clear the confirmed facts
            }
        ]
    },
)
print(response.context_management.applied_edits)   # what was cleared, and how many tokens
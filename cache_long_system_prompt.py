import anthropic

client = anthropic.Anthropic()
POLICY_MANUAL = open("policy_manual.md").read()   # large and identical on every call

def answer(question: str):
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=[
            {"type": "text", "text": "You answer staff questions using the policy manual."},
            {
                "type": "text",
                "text": POLICY_MANUAL,
                "cache_control": {"type": "ephemeral"},   # breakpoint: cache up to here
            },
        ],
        messages=[{"role": "user", "content": question}],  # changes on every call
    )
    u = response.usage
    print(f"written={u.cache_creation_input_tokens or 0} "
          f"read={u.cache_read_input_tokens or 0} "
          f"uncached={u.input_tokens} output={u.output_tokens}")
    return response

# Check the prefix is above the model's minimum cacheable length.
count = client.messages.count_tokens(
    model=MODEL,
    system=POLICY_MANUAL,
    messages=[{"role": "user", "content": "test"}],
)
print(count.input_tokens)
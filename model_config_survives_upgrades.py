import os
import anthropic

client = anthropic.Anthropic()

# Exact model IDs live in configuration, one per job, and change only through review.
MODELS = {
    "triage": os.environ["TRIAGE_MODEL_ID"],      # a Haiku model
    "drafting": os.environ["DRAFTING_MODEL_ID"],  # a Sonnet model
    "planning": os.environ["PLANNING_MODEL_ID"],  # an Opus model
}

INCOMPLETE = {"max_tokens", "refusal", "model_context_window_exceeded"}

def ask(job: str, prompt: str, effort: str | None = None) -> str:
    extra = {"output_config": {"effort": effort}} if effort else {}  # not every model supports effort
    response = client.messages.create(
        model=MODELS[job],
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
        **extra,
    )
    if response.stop_reason in INCOMPLETE:
        raise RuntimeError(f"{job}: incomplete response ({response.stop_reason})")
    # Newer models can return thinking blocks first, so never read content[0].
    return "".join(b.text for b in response.content if b.type == "text")
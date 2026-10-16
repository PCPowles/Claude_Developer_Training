import time
import anthropic

client = anthropic.Anthropic()

def tracked_call(step: str, **request):
    start = time.perf_counter()
    try:
        response = client.messages.create(**request)
    except anthropic.APIError as err:
        log_metric(step=step, error=type(err).__name__)
        raise
    u = response.usage
    log_metric(
        step=step,
        latency_ms=round((time.perf_counter() - start) * 1000),
        input=u.input_tokens,
        cache_write=u.cache_creation_input_tokens or 0,
        cache_read=u.cache_read_input_tokens or 0,
        output=u.output_tokens,
        stop_reason=response.stop_reason,
    )
    return response
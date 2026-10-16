import logging
import os
import anthropic

log = logging.getLogger("claude")
client = anthropic.Anthropic(max_retries=3, timeout=60.0)   # SDK retries 429, 5xx and connection errors
# MODEL = os.environ["CLAUDE_MODEL"]
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5") 

class TruncatedOutput(Exception):
    pass

def ask(messages, max_tokens=2048):
    try:
        response = client.messages.create(model=MODEL, max_tokens=max_tokens, messages=messages)
    except anthropic.BadRequestError as e:              # 400: fix the payload, do not retry
        log.error("invalid request: %s", e)
        raise
    except (anthropic.AuthenticationError, anthropic.PermissionDeniedError) as e:
        log.error("credential or access problem: %s", e)
        raise
    except anthropic.RateLimitError as e:               # still 429 after SDK retries
        log.warning("rate limited, queue for later: %s", e)
        raise
    except anthropic.APIConnectionError as e:           # network failure or timeout
        log.warning("network problem: %s", e)
        raise
    except anthropic.APIStatusError as e:               # any other status, including 5xx
        log.error("status=%s request_id=%s", e.status_code, e.response.headers.get("request-id"))
        raise

    log.info("request_id=%s stop_reason=%s input_tokens=%s output_tokens=%s",
             response._request_id, response.stop_reason,
             response.usage.input_tokens, response.usage.output_tokens)

    if response.stop_reason == "max_tokens":           # HTTP 200, output cut off
        raise TruncatedOutput("Raise max_tokens or split the input")
    if response.stop_reason == "refusal":
        raise RuntimeError("Claude declined; inspect stop_details")
    return response
import random
import time
import anthropic

client = anthropic.Anthropic(max_retries=0)       # this function is the only retry layer
RETRIABLE = {408, 409, 429, 500, 502, 503, 504, 529}

def create_with_retry(max_attempts=5, cap=30, **params):
    for attempt in range(1, max_attempts + 1):
        try:
            return client.messages.create(**params)
        except anthropic.APIStatusError as e:
            if e.status_code not in RETRIABLE or attempt == max_attempts:
                raise                              # terminal, or out of attempts
            wait = e.response.headers.get("retry-after")
        except anthropic.APIConnectionError:       # dropped connection or timeout
            if attempt == max_attempts:
                raise
            wait = None
        delay = float(wait) if wait else min(cap, 2 ** attempt) + random.uniform(0, 1)
        print(f"attempt {attempt} failed, waiting...") 
        time.sleep(delay)  # server's wait first, then capped backoff with jitter
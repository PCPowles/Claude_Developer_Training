"""Exercise every branch of ask() in sorted_failures_class.py.

Real API calls: success, 400, 401, 404, max_tokens (a few tokens each).
Offline (httpx mock / dead port): 429, 500, connection failure, refusal.

Run: venv\\Scripts\\python.exe demo_sorted_failures.py
"""
import logging

import anthropic
try:
    import httpx2 as httpx   # anthropic >= 1.13 in this venv uses httpx2, and plain httpx clients are rejected
except ImportError:
    import httpx

import sorted_failures_class as sf

logging.basicConfig(level=logging.INFO, format="    log: %(levelname)s %(message)s")

HELLO = [{"role": "user", "content": "Say hi in three words."}]
STORY = [{"role": "user", "content": "Write a 500 word story about a lighthouse."}]


def mock_client(status=200, body=None, headers=None):
    """Client whose HTTP layer returns a canned response. No retries so it fails fast."""
    def handler(request):
        return httpx.Response(status, json=body or {}, headers={"request-id": "req_mock123", **(headers or {})})
    return anthropic.Anthropic(api_key="fake", max_retries=0,
                               http_client=httpx.Client(transport=httpx.MockTransport(handler)))


def message_body(stop_reason):
    return {"id": "msg_mock", "type": "message", "role": "assistant", "model": "mock",
            "content": [{"type": "text", "text": "..."}], "stop_reason": stop_reason,
            "stop_sequence": None, "usage": {"input_tokens": 5, "output_tokens": 5}}


def error_body(kind, message):
    return {"type": "error", "error": {"type": kind, "message": message}}


# (label, client, model, messages, max_tokens, exception expected or None)
CASES = [
    ("success",
     anthropic.Anthropic(max_retries=0), sf.MODEL, HELLO, 100, None),
    ("400 bad request (empty messages)",
     anthropic.Anthropic(max_retries=0), sf.MODEL, [], 100, anthropic.BadRequestError),
    ("401 bad API key",
     anthropic.Anthropic(api_key="sk-ant-invalid", max_retries=0), sf.MODEL, HELLO, 100, anthropic.AuthenticationError),
    ("404 unknown model (falls through to APIStatusError)",
     anthropic.Anthropic(max_retries=0), "claude-does-not-exist", HELLO, 100, anthropic.APIStatusError),
    ("429 rate limited (mocked)",
     mock_client(429, error_body("rate_limit_error", "slow down")), sf.MODEL, HELLO, 100, anthropic.RateLimitError),
    ("500 server error (mocked)",
     mock_client(500, error_body("api_error", "boom")), sf.MODEL, HELLO, 100, anthropic.InternalServerError),
    ("connection failure (dead port)",
     anthropic.Anthropic(api_key="fake", base_url="http://127.0.0.1:9", max_retries=0), sf.MODEL, HELLO, 100,
     anthropic.APIConnectionError),
    ("max_tokens truncation (real, max_tokens=5)",
     anthropic.Anthropic(max_retries=0), sf.MODEL, STORY, 5, sf.TruncatedOutput),
    ("refusal stop_reason (mocked)",
     mock_client(200, message_body("refusal")), sf.MODEL, HELLO, 100, RuntimeError),
]


def main():
    real_client, real_model = sf.client, sf.MODEL
    results = []
    for label, client, model, messages, max_tokens, expected in CASES:
        print(f"\n== {label}")
        sf.client, sf.MODEL = client, model
        try:
            response = sf.ask(messages, max_tokens=max_tokens)
            ok = expected is None
            print(f"  returned: {response.content[0].text!r}" if ok else "  no exception raised")
        except Exception as e:
            ok = expected is not None and isinstance(e, expected)
            print(f"  raised {type(e).__name__}")
        results.append((label, ok))
        print(f"  {'PASS' if ok else 'FAIL'}")
    sf.client, sf.MODEL = real_client, real_model

    print("\n== summary")
    for label, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")


if __name__ == "__main__":
    main()

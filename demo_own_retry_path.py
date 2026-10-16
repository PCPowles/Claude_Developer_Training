from own_retry_path import create_with_retry
 
response = create_with_retry(
    model="claude-sonnet-5-5",
    max_tokens=200,
    messages=[{"role": "user", "content": "Tell me 3 cat jokes."}],
)
 
print(response.content[0].text)
print("stop_reason:", response.stop_reason)

import asyncio
import os
from anthropic import AsyncAnthropic

client = AsyncAnthropic()
# MODEL = os.environ["CLAUDE_MODEL"]
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5") 
in_flight = asyncio.Semaphore(8)        # cap concurrent requests

async def summarise(ticket: str) -> str:
    async with in_flight:
        response = await client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": f"Summarise this ticket in two sentences:\n\n{ticket}"}],
        )
    return "".join(b.text for b in response.content if b.type == "text")

async def main(tickets: list[str]) -> list[str]:
    return await asyncio.gather(*(summarise(t) for t in tickets))   # keeps input order

summaries = asyncio.run(main(load_tickets()))
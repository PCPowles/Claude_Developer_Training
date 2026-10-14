import asyncio
import json
import os
from pathlib import Path
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

def load_tickets(path: str = "tickets.json") -> list[str]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

if __name__ == "__main__":
    tickets = load_tickets()
    summaries = asyncio.run(main(tickets))
    for ticket, summary in zip(tickets, summaries):
        print(f"- {ticket}\n  => {summary}\n")
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage

async def main():
    options = ClaudeAgentOptions(max_turns=1)   # add model="haiku" etc. to test an alias
    async for message in query(prompt="Reply with just OK.", options=options):
        if isinstance(message, AssistantMessage):
            print("Model:", message.model)
            # break

asyncio.run(main())
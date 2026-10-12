# A supervisor with two read-only workers (Python)

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, ResultMessage

WORKERS = {
    "log-analyst": AgentDefinition(
        description="Reads service logs and reports error patterns. Use for any question about log contents.",
        prompt="You analyse log files. Report each distinct error with first and last timestamp and a count.",
        tools=["Read", "Grep", "Glob"],   # read-only
        model="haiku",                    # cheaper model for a narrow task
    ),
    "code-tracer": AgentDefinition(
        description="Finds the code that raises a given error message. Use after the error is known.",
        prompt="Trace the error message you are given to the code that raises it. Return file paths and line numbers.",
        tools=["Read", "Grep", "Glob"],
    ),
}

async def main():
    options = ClaudeAgentOptions(
        system_prompt=(
            "You coordinate an incident review and write the summary yourself. Workers cannot see "
            "this conversation, so give each one every path, time window and error message it needs."
        ),
        allowed_tools=["Read", "Grep", "Glob", "Agent"],
        agents=WORKERS,
        max_turns=30,
        env={"CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1"},   # workers may not spawn workers
    )
    try:
        async for message in query(
            prompt="Why did checkout fail between 02:00 and 03:00? Logs are in ./logs.",
            options=options,
        ):
            if isinstance(message, ResultMessage) and message.subtype == "success":
                print(message.result)
    except Exception as error:
        print(f"Run ended early: {error}")

asyncio.run(main())
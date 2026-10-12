import asyncio
from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server, query, ClaudeAgentOptions, ResultMessage

ORDERS = {"A100": "shipped", "A101": "processing"}   # stand-in for your order system

@tool("get_order_status", "Return the shipping status of one order. IDs look like A100.", {"order_id": str})
async def get_order_status(args: dict[str, Any]) -> dict[str, Any]:
    status = ORDERS.get(args["order_id"])
    if status is None:
        return {   # a clear error result lets Claude correct itself
            "content": [{"type": "text", "text": f"No order {args['order_id']}. Check the ID with the customer."}],
            "is_error": True,
        }
    return {"content": [{"type": "text", "text": f"Order {args['order_id']}: {status}"}]}

orders = create_sdk_mcp_server(name="orders", version="1.0.0", tools=[get_order_status])

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"orders": orders},
        tools=[],                                     # no file or shell tools for this agent
        allowed_tools=["mcp__orders__get_order_status"],
        permission_mode="dontAsk",                    # anything not pre-approved is denied
        setting_sources=[],                           # do not load CLAUDE.md or settings from this host
        max_turns=10,
    )
    try:
        async for message in query(prompt="Where are orders A100 and A999?", options=options):
            if isinstance(message, ResultMessage):
                print(message.subtype, message.result if message.subtype == "success" else "")
    except Exception as error:
        print(f"Run stopped: {error}")

asyncio.run(main())
from Agent_With_Checks import run

CONFIG = {"timeout": 30, "retries": 1}

tools = [
    {"name": "read_config", "description": "Return the current config as JSON.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "write_config", "description": "Set one config key to a new value.",
     "input_schema": {"type": "object",
                      "properties": {"key": {"type": "string"}, "value": {"type": "integer"}},
                      "required": ["key", "value"]}},
]

def execute(name, args):
    if name == "read_config":
        return str(CONFIG)
    
    if name == "write_config":
        CONFIG[args["key"]] = args["value"]
        return f"Set {args['key']} = {args['value']}"
    
    return f"Unknown tool {name}"

def approve(name, args):
    return input(f"Allow {name}({args})? [y/N] ").strip().lower() == "y"

response = run("Requests are timing out. Fix the config.", tools, execute, approve)
for block in response.content:
    if block.type == "text":      # skip thinking blocks, which have no .text
        print(block.text)
print(CONFIG)

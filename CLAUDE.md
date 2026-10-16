# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal workspace for Claude developer-certification training (Anthropic SDK and Claude Agent SDK). It is a flat collection of standalone lab scripts, not an application. There is no build system, test suite, linter, `requirements.txt` or README. The `.xlsx` files (~90 MB each, dated by day) and the `.docx` are study notes and are tracked in git; don't open or rewrite them.

## Running things

- Windows + PowerShell. The interpreter is the repo-local venv: `venv\Scripts\python.exe` (wired up in `.vscode/settings.json` for both the Python extension and Code Runner).
- Run a script from the repo root: `venv\Scripts\python.exe <script>.py`. Each script is independent and has no test harness.
- `ANTHROPIC_API_KEY` must be set (or an `ant auth login` profile). `CLAUDE_MODEL` is optional; scripts default to `claude-sonnet-5-5`. Every run makes real, billed API calls.
- `AnthropicVertex` is used when `USE_VERTEX` is set, together with `GCP_PROJECT` (`api_mechanics_with_thinking.py`).
- Two different SDKs are in use. The `anthropic` package covers the Messages API. `claude_agent_sdk` is needed by `Agent_Architecture.py`, `1_Agent_Architecture.py`, `2_Agent_Construction.py` and `check_model.py`. Check which one a script imports before assuming what's installed.

## Layout and how the scripts relate

- **Messages API labs**: `api_mechanics*.py`, `step1_first_message_call*.py`, `async_calls.py`, `check_model_requirements.py`. These cover streaming, adaptive thinking, prompt caching, image input, the async + `Semaphore` pattern, and preflight checks (capabilities via `models.retrieve`, headroom via `count_tokens`). Shared inputs sit beside them: `extraction_rules.txt` (system prompt), `invoice.png`, `largest_case.txt`, `tickets.json`.
- **Agent loop labs**: `Agent_With_Checks.py` holds the hand-written tool-use loop. It adds a `MAX_STEPS` cap and a `NEEDS_APPROVAL` set of tools that go through an `approve()` callback, and returns the final response so the caller inspects `stop_reason`. `demo_agent.py` imports `run` from it and supplies the tools, `execute` and `approve`, with a human `input()` prompt.
- **Supervisor lab**: `Agent_Architecture.py` uses the Claude Agent SDK with a coordinator and two read-only subagents (`log-analyst`, `code-tracer`). It investigates the incident in `logs/` and `src/`, and `config/payment.yaml` is the config tied to that incident. Those sample files are generated and committed from `make_samples.py` (re-running it overwrites them), so edit the generator if you want a lasting change.
- **Custom tool lab**: `2_Agent_Construction.py` is a separate Agent SDK script (not a copy of the above). It defines a `@tool` function and exposes it through `create_sdk_mcp_server`.
- **Course scaffolding**: `lab_runtime.py` is a stub of the course's `step_header`, `exam_note`, `pitfall` and `checkpoint` helpers. `step1_first_message_call.py` expects the real one at `../shared`, so it is a partly scaffolded exercise with its solution commented out in a string block.
- **Reference docs**: `.claude/rules/requirements.yaml` is a sample requirements spec (functional checks versus infrastructure constraints). `.claude/rules/eval_gate.py` is a sample CI eval gate. It reads `prompts/classifier_v7.txt` and `evals/classifier.jsonl`, which do not exist in this repo, so it cannot run as-is. `agent_platform_decision.html` is a static decision aid.
- `.claude/agents/code-improver.md` is a read-only reviewer subagent (Read, Grep and Glob only).

## Gotchas

- **Duplicates**: several files are copies kept side by side (`Agent_Architecture.py` and `1_Agent_Architecture.py`, `Agent_With_Checks.py` and `2_Agent_With_Checks.py`, `Claude_API_Mechanics.py` and `api_mechanics.py`). `demo_agent.py` imports the unnumbered `Agent_With_Checks`, so changes to the loop go there; update the copy too if you want them to stay in sync.
- **Snapshot**: `async_calls_base.py` is the original snippet and calls an undefined `load_tickets()`. `async_calls.py` is the runnable version.
- **Model IDs**: use the current ones (for example `claude-sonnet-5-5`, `claude-haiku-5-5`, `claude-opus-5-5`) and never append date suffixes. On current models do not send `budget_tokens` (use `thinking={"type": "adaptive"}`, with `"display": "summarized"` if you want readable thinking), do not prefill assistant turns, and do not use forced `tool_choice`.
- `__pycache__/` and `~$*.xlsx` Office lock files are tracked and there is no `.gitignore`. Don't commit new ones.

"""
 Memory location:
 C:\Users\pcpow\claude\projects\c--dev-Claude-Developer-Training\
 memory\MEMORY.md

 View Output from Python Program:
  claude -p async_calls.py --output-format stream-json --verbose

"""


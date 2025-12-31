# LangChain Recommendation Agent ⚡️

A small example project that demonstrates how to create a structured-output agent using LangChain and Ollama. The agent calls simple Python tools to gather user history and store inventory, then recommends 3 items.

---

## Features ✅

- Uses LangChain (core) to create an agent with tool support
- Uses Ollama via `langchain_ollama` as the LLM backend
- Demonstrates structured output via a Pydantic model (`RecommendedUserItems`)
- Simple tools: `get_user_history`, `get_store_inventory`, `rank_items`

---

## Requirements 🔧

- Python 3.10+
- Ollama (running locally if you use the same configuration as `main.py`)
- Project dependencies listed in `requirements.txt`

---

## Quick setup (Windows) 💡

1. Create & activate a virtual environment

```powershell
python -m venv langchainapp
& .\langchainapp\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Ensure Ollama is running and that the model referenced in `main.py` (by default `gpt-oss:20b`) is available and the server is reachable at `http://localhost:11434/`.

- Example Ollama steps (if you use Ollama):
  - Install Ollama: https://ollama.ai/docs
  - Pull the model if needed: `ollama pull gpt-oss:20b`
  - Run Ollama (server): `ollama serve`

> Note: `main.py` currently constructs the `ChatOllama` client with a hard-coded `base_url` and model. You can change those values or use environment variables if you prefer.

---

## Running the example ▶️

```powershell
python main.py
```

The script will create an agent, invoke it with a sample user request (see `main.py`) and print messages returned by the agent. The output demonstrates tool calls and the agent's `ToolMessage` for `rank_items`.

Example expected behavior (simplified):

- Agent calls `get_user_history("Richard")`
- Agent calls `get_store_inventory("Store ABC")`
- Agent calls `rank_items(...)` and returns a structured result containing `items: ["Keyboard","Mouse","Mousepad"]`

---

## How it works (brief) 🧠

- Tools are normal Python functions decorated with `@tool` from `langchain_core.tools`.
- The agent is built with `create_agent(...)` and uses `ToolStrategy` with a Pydantic model `RecommendedUserItems` for structured output.
- The LLM backend is `ChatOllama` and can be configured with a different model or base URL.

---

## Extending this project ✨

- Add more realistic implementations for the tools (database queries, real inventory APIs).
- Replace the hard-coded model and base URL with environment variables (use `.env` + `python-dotenv` already in the project).
- Add unit tests for the tools and integration tests for agent behavior.

---

## Relation to LangGraph

This project uses a single LangChain agent with tool calls. For more complex or multi-agent workflows, this design would naturally migrate to LangGraph, where:
- Each tool call becomes an explicit node
- State (user context, inventory, ranked items) is shared across nodes
- Execution order and branching are deterministic and inspectable

---

## License & Author

- Author: Richard (local project)

---

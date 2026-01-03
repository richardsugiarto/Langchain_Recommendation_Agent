# LangChain / LangGraph Recommendation Agent ⚡️

This project demonstrates two complementary approaches to building a recommendation system using
LangChain, Ollama, and LangGraph:

1. **Structured-output LangChain Agent** (`main.py`)
2. **Deterministic LangGraph Workflow** (`graph.py`) with JSON-backed user + store data

Both versions use simple Python tools to fetch purchase history, get store inventory, and rank candidate items.

---

## ✨ What’s Included

### ✅ LangChain Agent (single-agent tool-calling)

- Structured Pydantic output (`RecommendedUserItems`)
- Tool calls handled implicitly by the agent
- Good for prototyping and experimentation

File: `main.py`

---

### 🧩 LangGraph Recommendation Pipeline (enhanced)

A more realistic, production-style workflow:

- User history + inventory loaded from JSON files
- Runtime arguments (username, store, top-k)
- Deterministic node execution
- Explicit state passing between nodes
- DB-ready data-loading layer

File: `graph.py`

Graph stages:

1. `fetch_user_history`
2. `fetch_inventory`
3. `build_candidates` (LLM selects likely next items)
4. `recommend_items` (rank + return top-K)

Output is returned as a structured `RecommendationResult`.

---

## 📂 Data Files

Located in `data/`:

- `users.json`
- `stores.json`

These simulate persistence and can later be replaced with a database.

Example structure:

```json
[
  {
    "username": "richard",
    "name": "Richard Sugiarto",
    "items": ["Keyboard", "Mouse", "Headset"]
  }
]
```
## 🔧 Requirements

Python 3.10+

Ollama running locally

Model available in Ollama (default: gpt-oss:20b)

python-dotenv for environment loading

Install dependencies:

```pip install -r requirements.txt```


Ensure Ollama model exists:

```ollama pull gpt-oss:20b```

## ▶️ Running the LangChain Agent (main.py)

Runs a single agent that calls tools automatically:

```python main.py```


Behavior (simplified):

```Calls get_user_history

Calls get_store_inventory

Calls rank_items

Returns structured items=[...]
```

## ▶️ Running the LangGraph Workflow (graph.py)

Supports runtime arguments:

``` python graph.py --username richard --store ABC --top-k 3 ```


Example output:

``` Recommended items: ["Monitor", "Headset", "Webcam"] ```


This version is closer to a real production pipeline because:

tools are deterministic

state is explicit + inspectable

execution order is guaranteed

data sources can be swapped for a DB

## 🧠 How Recommendations Work

Both implementations follow the same conceptual flow:

```
Fetch prior purchased items

Fetch available store inventory

Select promising candidate items

Rank items + return top-K
```

The LangGraph version delegates candidate selection to the LLM, while ranking remains a simple mock function.

## 🚀 Future Improvements

Replace JSON files with database storage

Support multiple stores per user

Extend LangGraph with branches or retries

## 👤 Author

Richard
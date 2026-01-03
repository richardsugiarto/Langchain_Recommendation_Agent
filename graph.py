"""
Portfolio Project: LangGraph-based Recommendation Agent (Enhanced)
-------------------------------------------------
Enhancements:
- User purchase history stored as JSON (array of dicts)
- Store inventory stored as JSON (array of dicts)
- Username passed as runtime argument
- Data-loading layer simulating real-world persistence (DB-ready)

This keeps the project simple while making it closer to a real application.
"""

from typing import List, TypedDict, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END

# --------------------
# Environment
# --------------------
load_dotenv()

llm = ChatOllama(
    model="gpt-oss:20b",
    base_url="http://localhost:11434/",
    validate_model_on_init=True,
    temperature=0,
)

DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"
STORES_FILE = DATA_DIR / "stores.json"

# --------------------
# Domain Models
# --------------------

class RecommendationResult(BaseModel):
    """Final structured recommendation output."""
    items: List[str] = Field(description="Top recommended items for the user")


class UserPurchase(BaseModel):
    username: str
    name: str
    items: List[str]


class StoreInventory(BaseModel):
    store_id: str
    store_name: str
    items: List[str]


class AgentState(TypedDict):
    username: str
    store_id: str
    top_k: int
    user_history: List[str]
    inventory: List[str]
    candidate_items: List[str]
    result: Optional[RecommendationResult]

# --------------------
# Data Loading Utilities
# --------------------

def load_users() -> List[UserPurchase]:
    with open(USERS_FILE, "r") as f:
        data = json.load(f)
    return [UserPurchase(**u) for u in data]


def load_stores() -> List[StoreInventory]:
    with open(STORES_FILE, "r") as f:
        data = json.load(f)
    return [StoreInventory(**s) for s in data]

# --------------------
# Tools
# --------------------

@tool

def get_user_history(username: str) -> List[str]:
    """Fetch previously purchased items for a given username."""
    users = load_users()
    for user in users:
        if user.username == username:
            return user.items
    return []


@tool

def get_store_inventory(store_id: str) -> List[str]:
    """Fetch available items for a given store."""
    stores = load_stores()
    for store in stores:
        if store.store_id == store_id:
            return store.items
    return []


@tool

def rank_items(items: List[str]) -> List[str]:
    """Rank candidate items and return top 3 (mock logic)."""
    return sorted(items)[:3]

# --------------------
# Graph Nodes
# --------------------

def fetch_user_history(state: AgentState) -> AgentState:
    state["user_history"] = get_user_history.invoke(state["username"])
    return state


def fetch_inventory(state: AgentState) -> AgentState:
    state["inventory"] = get_store_inventory.invoke(state["store_id"])
    return state


def build_candidates(state: AgentState) -> AgentState:
    """Use LLM (Ollama) to select relevant candidate items."""

    prompt = f"""
    You are a recommendation system.

    User previously bought:
    {state['user_history']}

    Available store inventory:
    {state['inventory']}

    Select items that the user is most likely interested in next.
    Return only a JSON list of item names.
    """

    response = llm.invoke(prompt)
    try:
        state["candidate_items"] = json.loads(response.content)
    except Exception:
        state["candidate_items"] = []

    return state


def recommend_items(state: AgentState) -> AgentState:
    """Rank and return top-K recommendations."""
    ranked = rank_items.invoke( {"items": state["candidate_items"]})
    state["result"] = RecommendationResult(items=ranked[: state["top_k"]])
    return state

# --------------------
# LangGraph Definition
# --------------------

graph = StateGraph(AgentState)

graph.add_node("fetch_user_history", fetch_user_history)
graph.add_node("fetch_inventory", fetch_inventory)
graph.add_node("build_candidates", build_candidates)
graph.add_node("recommend_items", recommend_items)

graph.set_entry_point("fetch_user_history")
graph.add_edge("fetch_user_history", "fetch_inventory")
graph.add_edge("fetch_inventory", "build_candidates")
graph.add_edge("build_candidates", "recommend_items")
graph.add_edge("recommend_items", END)

app = graph.compile()

# --------------------
# Run Example
# --------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LangGraph Recommendation Agent")
    parser.add_argument("--username", required=True, help="Username to recommend items for")
    parser.add_argument("--store", default="ABC", help="Store ID")
    parser.add_argument("--top-k", type=int, default=3, help="Number of items to recommend")
    args = parser.parse_args()

    initial_state: AgentState = {
        "username": args.username,
        "store_id": args.store,
        "top_k": args.top_k,
        "user_history": [],
        "inventory": [],
        "candidate_items": [],
        "result": None,
    }

    final_state = app.invoke(initial_state)
    print("Recommended items:", final_state["result"].items)

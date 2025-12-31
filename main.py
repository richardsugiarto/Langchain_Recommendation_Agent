from langchain_core.tools import tool
import json
from langchain_ollama import ChatOllama
from langchain.messages import AIMessage,ToolCall,ToolMessage
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel,Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy,ProviderStrategy

load_dotenv()
# --------------------
# Tools the agent can use
# --------------------

#Structured Output
class RecommendedUserItems(BaseModel):
    """List of items recommendation for a user."""
    items: List[str] = Field(description="List of recommended items")

get_user_history_label = "get_user_history"
@tool("get_user_history")
def get_user_history(username: str) -> List[str]:
    """Get list of items a user has bought before.
    
    Args:
        username (str): the username.
    """
    return ["Keyboard", "Gaming Mouse", "Mousepad"]

get_store_inventory_label = "get_store_inventory"
@tool("get_store_inventory")
def get_store_inventory(storeid: str) -> List[str]:
    """Get list of available items in the store.
    
    Args:
        storeid (str): store id
    """
    return ["Keyboard", "Gaming Mouse", "Mousepad", "Monitor", "Headset", "Webcam"]

rank_items_label = "rank_items"
@tool("rank_items")
def rank_items(candidate_items: List[str]) -> List[str]:
    """Rank candidate items and return top 3.
    
    Args:
        candidate_items List[str]: List of candidate items
    """
    return sorted(candidate_items)[:3]


tools = [get_user_history, get_store_inventory, rank_items]

# --------------------
# Agent LLM (brain)
# --------------------
llm = ChatOllama(model="gpt-oss:20b",base_url="http://localhost:11434/",validate_model_on_init=True,
    temperature=0,
)

# --------------------
# Create the agent
# --------------------


prompt = """
You are a helpful recommendation AI.
You may call tools to gather user history and store inventory.
After gathering data, recommend 3 items for the user.
"""
agent = create_agent(model=llm,tools=tools,system_prompt=prompt,response_format=ToolStrategy(RecommendedUserItems))

# --------------------
# Ask the agent to recommend items
# --------------------

result = agent.invoke({
    "messages":[{"role":"user","content":"Reccomend 3 items for Richard from Store ABC."}]
    })

if result:
    for chunk in result["messages"]:
        if isinstance(chunk,ToolMessage) and chunk.name == rank_items_label:
            print(chunk)

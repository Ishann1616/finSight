import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from agent.tools import (
    get_spending_summary,
    get_recent_transactions,
    get_monthly_total
)

def get_agent_executor(user_id:int) :
    llm= ChatOpenAI(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )

    tools=[
        get_spending_summary,
        get_recent_transactions,
        get_monthly_total
    ]
    
    agent = create_react_agent(llm,tools=tools)
    return agent
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from agent.tools import (
    get_spending_summary,
    get_recent_transactions,
    get_monthly_total
)

def get_agent_executor(user_id:int) :
    llm= ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        google_api_key= os.getenv("GOOGLE_API_KEY"),
        convert_system_message_to_human=True
    )

    tools=[
        get_spending_summary,
        get_recent_transactions,
        get_monthly_total
    ]
    
    agent = create_react_agent(llm,tools=tools)
    return agent
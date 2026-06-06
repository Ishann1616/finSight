from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent,AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import hub
from agent.tools import (
    get_spending_summary,
    get_recent_transactions,
    get_monthly_total
)
import os
from dotenv import load_dotenv
load_dotenv()

def get_agent_executor(user_id:int) -> AgentExecutor:
    llm= ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key= os.getenv("GOOGLE_API_KEY")
    )

    tools=[
        get_spending_summary,
        get_recent_transactions,
        get_monthly_total
    ]

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    prompt =hub.pull("hwchase17/react-chat")

    agent = create_react_agent(llm,tools,prompt)

    executor = AgentExecutor(
        agent= agent,
        tools= tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )

    return executor
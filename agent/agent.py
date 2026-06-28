import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from agent.tools import (
    get_spending_summary,
    get_recent_transactions,
    get_monthly_total,
    semantic_search_transactions,
    check_affordability,
    get_sip_summary,
    calculate_sip_corpus,
    get_fund_recommendations,
    get_emi_summary,
    get_tax_estimate,
    get_loan_advice,
    get_bank_recommendations
)
from agent.memory import load_history, save_message

def get_agent_executor(user_id:int) :
    llm= ChatOpenAI(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )

    tools=[
        get_spending_summary,
        get_recent_transactions,
        get_monthly_total,
        semantic_search_transactions,
        check_affordability,
        get_sip_summary,
        calculate_sip_corpus,
        get_fund_recommendations,
        get_emi_summary,
        get_tax_estimate,
        get_loan_advice,
        get_bank_recommendations
    ]
    
    agent = create_react_agent(llm,tools=tools)
    return agent

def run_agent(user_id: int, message: str) -> str:
    agent = get_agent_executor(user_id)

    history=load_history(user_id)

    messages =[]
    for m in history:
        if m["role"] == "human":
            messages.append(HumanMessage(content=m["content"]))
        else:
            messages.append(AIMessage(content=m["content"]))

    messages.append(HumanMessage(content=f"[user_id: {user_id}] {message}"))

    response = agent.invoke({"messages":messages})
    answer = response["messages"][-1].content

    save_message(user_id,"human",message)
    save_message(user_id,"assistant",answer)

    return answer

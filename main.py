import os, json
from dotenv import load_dotenv; load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage

from tools import tools
from schema import AnalysisOutput

SYSTEM_PROMPT = """You are an AI Data Analyst.

Workflow:
1) Parse the user's question.
2) If it's a numeric summary -> call quick_stats.
3) If filtering rows -> call query_data.
4) If trend or chart -> call plot_timeseries.
5) Always return ONLY valid JSON matching the AnalysisOutput schema.
Never output anything except the JSON object.
"""

def build_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    parser = PydanticOutputParser(pydantic_object=AnalysisOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(llm,tools,prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return executor, parser

def main():
    executor, parser = build_agent()

    chat_history = []
    print("📊 AI Data Analyst (type 'exit' to quit)")
    while True:
        try:
            q = input("\nYou: ")
        except EOFError:
            break
        if q.strip().lower() == "exit":
            break

        chat_history.append(HumanMessage(content=q))
        resp = executor.invoke({"query": q, "chat_history": chat_history})
        raw = resp.get("output", "")
        try:
            ans = parser.parse(raw)
            print("\n📈 Insight:", ans.answer)
            if ans.chart_path:
                print("Chart saved ->", ans.chart_path)
            chat_history.append(AIMessage(content=ans.answer))
        except Exception as e:
            print("Parse error:", e)
            print("Raw model output:", raw)

if __name__ == "__main__":
    main()

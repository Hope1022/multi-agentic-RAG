from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import os
from llm import groq_llm as llm
from dotenv import load_dotenv
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("groq_api_key")
serper = GoogleSerperAPIWrapper()

# llm = ChatGroq(api_key=GROQ_API_KEY,
#                model="llama-3.1-8b-instant")


def search_web(query: str) ->str:
    
    results = serper.run(query)
    return results

PLAN_SYSTEM_PROMPT = """You are an academic coach.
Build a realistic study plan user specific based only on using the given Student question,
Student performance context,Curriculum priority context, Relevant web_search results.
Return findings in this exact format:

WEEK 1: one sentence focus
WEEK 2: one sentence focus
WEEK 3: one sentence focus
DAILY TIME: how many hours per day
PREDICTED OUTCOME: one sentence

Max 5 lines total."""

def parse_instruction(instructions: str, agent: str) -> str:
    for line in instructions.split("\n"):
        if line.startswith(f"{agent}:"):
            return line.replace(f"{agent}:", "").strip()
    return instructions

def study_plan_node(state):
    question     = state["question"]
    instructions = parse_instruction(state["supervisor_instructions"],"STUDY_PLAN")
    performance  = state.get("performance_result", "")
    curriculum  = state.get("curriculum_result", "")
    web_scrape = search_web(instructions)
    

    prompt = f"""Student question: {question}

Your specific task or instruction: {instructions}
Student performance context:{performance}

Curriculum priority context:{curriculum}
Relevant web_search results:
{web_scrape}


Analyze these results and return your findings."""

    response = llm.invoke([
        SystemMessage(content=PLAN_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])

    return {"study_plan": response.content}    
question = "I failed my calculus midterm. What do I do?"
instructions = "find 3 week recovery strategies"
web_scrape = search_web(instructions)
prompt = f"""Student question: {question}

Your specific task or instruction: {instructions}

Relevant web_search results:
{web_scrape}

Analyze these results and return your findings."""

# system_message =SystemMessage(content=PLAN_SYSTEM_PROMPT)
# human_message = HumanMessage(content=prompt)
# messages = [system_message,human_message]
# full_chain = llm|StrOutputParser()
# result = full_chain.invoke(messages)
# print(result)
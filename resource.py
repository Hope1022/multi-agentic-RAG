from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from llm import gemini_llm as llm
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("groq_api_key")
serper = GoogleSerperAPIWrapper()

# llm = ChatGroq(api_key=GROQ_API_KEY,
#                model="llama-3.1-8b-instant")
# from langchain_google_genai import ChatGoogleGenerativeAI
# llm = ChatGoogleGenerativeAI(
#     google_api_key=os.getenv("GEMINI_API_KEY"),
#     model="gemini-2.0-flash"
# )


def search_web(query: str) ->str:
    
    results = serper.run(query)
    return results

RESOURCE_SYSTEM_PROMPT = """You are a learning resource curator.
Find the best resources for the student's specific gap.be specific to a given Student performance and Curriculum priority Contexts 
Return findings in this exact format:

RESOURCE 1: name and why it helps
RESOURCE 2: name and why it helps
RESOURCE 3: name and why it helps

Only recommend real, specific, freely available and user specific resources. Max 3 lines total."""

def parse_instruction(instructions: str, agent: str) -> str:
    for line in instructions.split("\n"):
        if line.startswith(f"{agent}:"):
            return line.replace(f"{agent}:", "").strip()
    return instructions

def resource_node(state):
    question     = state["question"]
    instructions = parse_instruction(state["supervisor_instructions"],"RESOURCE")
    performance      = state.get("performance_result", "")
    curriculum       = state.get("curriculum_result", "")
    web_scrape = search_web(instructions)
    

    prompt = f"""Student question: {question}

Your specific task or instruction: {instructions}
Student performance context:{performance}

Curriculum priority context:{curriculum}
Relevant web_search results:
{web_scrape}

Analyze these results and return your findings."""

    response = llm.invoke([
        SystemMessage(content=RESOURCE_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])

    return {"resource": response.content}    
# question = "I failed my calculus midterm. What do I do?"
# instructions = "find integration tutorials"
# web_scrape = search_web(instructions)
# prompt = f"""Student question: {question}

# Your specific task or instruction: {instructions}

# Relevant web_search results:
# {web_scrape}

# Analyze these results and return your findings."""

# system_message =SystemMessage(content=RESOURCE_SYSTEM_PROMPT)
# human_message = HumanMessage(content=prompt)
# messages = [system_message,human_message]
# full_chain = llm|StrOutputParser()
# result = full_chain.invoke(messages)
# print(result)


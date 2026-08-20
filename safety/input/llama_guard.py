import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("groq_api_key")

guard_llm = ChatGroq(model="meta-llama/llama-prompt-guard-2-86m",
                     api_key=groq_api_key)

def llamaguard_node(state: dict) -> dict:
    question = state["question"]

    response = guard_llm.invoke([
        {"role": "user", "content": question}
    ])

    if response.content.strip().lower().startswith("unsafe"):
        return {"is_safe": False, "draft_answer":"(llama_guard)bad input!, please send your question again"}

    return {"is_safe": True}
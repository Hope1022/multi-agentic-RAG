import os
from headroom.tokenizers import TiktokenCounter
import tiktoken

tokenizer = TiktokenCounter("cl100k_base")
from headroom import compress
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import chromadb
from dotenv import load_dotenv
# from headroom import Smartcrusher
from headroom.integrations.langchain import HeadroomChatModel
from headroom.transforms.smart_crusher import SmartCrusher
#from llm import gemini_llm as llm
from llm import llm_gemini as llm
# if os.getenv("HF_TOKEN"):
#     os.environ["HUGGINGFACE_HUB_TOKEN"] = os.getenv("HF_TOKEN")

    
load_dotenv()
GROQ_API_KEY = os.getenv("groq_api_key")
# llm = ChatGroq(
#     api_key=GROQ_API_KEY,
#     model="llama-3.1-8b-instant"
# )

# def token_minimization(output:str)->str:
#     messages = [
#         {
#             "role": "tool",
#             "content": output,
#             "tool_call_id": "retrieval_1"
#         }
#     ]

#     result = compress(messages, model="gpt-4o", config=config)  
    
#     print(f"tokens saved: {result.tokens_saved}")
#     return result.messages[0]["content"]

CURRICULUM_SYSTEM_PROMPT = """You are a course content expert.
Analyze only the given document chunks.
Return findings in this exact format:

HIGHEST PRIORITY: one sentence
WHAT TO FOCUS ON: one sentence
WHAT TO SKIP: one sentence
EXAM TIP: one sentence

Never add information not found in the documents, never ask a question. Max 4 lines total."""
prompt_template = ChatPromptTemplate.from_messages([
  ("system",CURRICULUM_SYSTEM_PROMPT),
  ("human","{input}")
])
full_chain = prompt_template|llm|StrOutputParser()
def search_course_materials(query: str) -> str:
  embeddings =OllamaEmbeddings(model="nomic-embed-text")
  current_dir = os.path.dirname(os.path.abspath(__file__))
  project_root = os.path.dirname(current_dir) 
  persistent_directory = os.path.join(project_root, "resources", "db", "chroma_db")
  client = chromadb.PersistentClient(path=persistent_directory)
    
  db = Chroma(
            client=client,               
            collection_name="odyssey",    
            embedding_function=embeddings
        )
    
  retriever = db.as_retriever(
  search_type="similarity_score_threshold",
  search_kwargs={"k": 5, "score_threshold": 0.38}, #the more threshold
    #the more super close
 )
  results = retriever.invoke(query)
  output = ""
  for doc in results:
    output += doc.page_content + "\n---\n"
        # doc.page_content = the actual text chunk
#         # we join all 4 chunks into one string
        
#     crusher = SmartCrusher()
#     messages = [
#     {"role": "tool", "content": output}
# ]
#     compressed = crusher.apply(messages,tokenizer=tokenizer)
    return output
# query = "find what topics are on the final exam and what carries most weight"
# result = search_course_materials(query)
# print(result)
# print(search_course_materials(query))
def parse_instruction(instructions: str, agent: str) -> str:
    for line in instructions.split("\n"):
        if line.strip().startswith(f"{agent}:"):
            return line.replace(f"{agent}:", "").strip()
    return instructions

def curriculum_node(state):
    question    = state["question"]
    instructions = state["supervisor_instructions"]
    

    instruction = parse_instruction(instructions, "CURRICULUM")

    chunks = search_course_materials(instruction)
    

    prompt = f"""Student question: {question}

Your specific task: {instruction}

Relevant course document chunks:
{chunks}

Analyze these documents and return your findings."""

    response = full_chain.invoke(
      {"input",prompt}
    )
    return {"curriculum_result": response}

#Testing
# query = "find what topics are on the final exam and what carries most weight"
# state = {
#     "question": query,
#     "supervisor_instructions": """PERFORMANCE: find scores and attendance
# CURRICULUM: find final exam topics
# RESOURCE: find integration tutorials
# STUDY_PLAN: find 3 week recovery plan"""
# }
# print(parse_instruction(state["supervisor_instructions"],"CURRICULUM"))
# result = curriculum_node(state)
# print(result)

from langsmith import Client
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "")

client = Client()
print("Connected:", client.list_projects())

# import headroom


# print(headroom.__version__)

# test with guaranteed large JSON content
# fake_json = str([{"id": i, "score": i*10, "subject": "calculus", "attendance": True, "notes": "student was present and participated actively in class discussions"} for i in range(100)])

# messages = [
#         {
#             "role": "tool",
#             "content": fake_json,
#             "tool_call_id": "retrieval_1"
#         }
#     ]

# result = compress(messages, model="gpt-4o", config=config)

# print(f"version       : {headroom.__version__}")
# print(f"tokens before : {result.tokens_before}")
# print(f"tokens after  : {result.tokens_after}")
# print(f"tokens saved  : {result.tokens_saved}")
# ind= "For each flagged subject, locate the current syllabus, associated study guides, and any past exams or practice quizzes; highlight the sections that correspond to the low‑scoring topics identified in the performance data"

# print()
# def test():
#   chunks = search_course_materials(ind)
#   specfic_task = ind
  
#   prompt = f"""Student question: {"i am failing at my course, what should i do?"}
  
#   Your specific task: {specfic_task}
  
#   Relevant course document chunks:
#   {chunks}
  
#   Analyze these documents and return your findings."""
  
#   response = full_chain.invoke(
#         {"input":prompt}
#       )
#   return response

# print(test())
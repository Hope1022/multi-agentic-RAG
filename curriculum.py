import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import chromadb
from dotenv import load_dotenv
from llm import gemini_llm as llm
load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model="llama-3.3-70b-versatile"
# )

CURRICULUM_SYSTEM_PROMPT = """You are a course content expert.
Analyze only the given document chunks.
Return findings in this exact format:

HIGHEST PRIORITY: one sentence
WHAT TO FOCUS ON: one sentence
WHAT TO SKIP: one sentence
EXAM TIP: one sentence

Never add information not found in the documents. Max 4 lines total."""

def search_course_materials(query: str) -> str:
    embeddings =OllamaEmbeddings(model="nomic-embed-text")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persistent_directory = os.path.join(current_dir, "db", "chroma_db")
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
        # we join all 4 chunks into one string

    return output
# query = "find what topics are on the final exam and what carries most weight"
# result = search_course_materials(query)
# print(result)
# print(search_course_materials(query))
def parse_instruction(instructions: str, agent: str) -> str:
    for line in instructions.split("\n"):
        if line.startswith(f"{agent}:"):
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

    response = llm.invoke([
        SystemMessage(content=CURRICULUM_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])

    return {"curriculum_result": response.content}

#Testing
# query = "find what topics are on the final exam and what carries most weight"
# state = {
#     "question":query,
#     "supervisor_instructions":"PERFORMANCE: find scores and attendance CURRICULUM: find final exam topics RESOURCE: find integration tutorials STUDY_PLAN: find 3 week recovery plan"
    
# }
# result = curriculum_node(state)
# print(result)
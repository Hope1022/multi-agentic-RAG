import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import ChatCohere
from dotenv import load_dotenv
load_dotenv()
groq_llm = ChatGroq(
    api_key=os.getenv("groq_api_key"),
    model="openai/gpt-oss-120b"
)

gemini_llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-3.6-flash"
)

cohere_llm = ChatCohere(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    model="command-a-03-2025"
)

llm = groq_llm.with_fallbacks([gemini_llm, cohere_llm])       
llm_gemini = gemini_llm.with_fallbacks([groq_llm, cohere_llm]) 
llm_cohere = cohere_llm.with_fallbacks([groq_llm, gemini_llm])


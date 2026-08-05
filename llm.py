import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import ChatCohere
from dotenv import load_dotenv
load_dotenv()
groq_llm = ChatGroq(
    api_key=os.getenv("groq_api_key"),
    model="llama-3.3-70b-versatile"
)

gemini_llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-2.0-flash"
)

cohere_llm = ChatCohere(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    model="command-a-03-2025"
)

#llm = groq_llm.with_fallbacks([gemini_llm, cohere_llm])

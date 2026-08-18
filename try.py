from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("groq_api_key")

llm = ChatGroq(
    model="openai/gpt-oss-120b", 
    api_key=groq_api_key
)

print(llm.invoke("hi"))

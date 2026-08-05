import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
#from langchain_pypdf import PyPDFLoader

load_dotenv()
groq_api_key = os.getenv("groq_api_key")

llm = ChatGroq(
    model ="llama-3.3-70b-versatile",
    api_key=groq_api_key
)

current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_files = [
    os.path.join(current_dir, "pdf's", "math101_syllabus.pdf"),
    os.path.join(current_dir, "pdf's", "math101_study_guide.pdf"),
    os.path.join(current_dir, "pdf's", "math101_past_exam.pdf")
]

persistent_directory = os.path.join(current_dir, "db", "chroma_db")


embeddings =OllamaEmbeddings(model="nomic-embed-text")
# message = [("system","you are an helpful RAG system, that takes a closely related words from a retrieved information which is '{related_chunks}', and using that information you will summarize and answer based on user's question"),("human","{question}")]
# prompt_template = ChatPromptTemplate.from_messages(message)

if not os.path.exists(persistent_directory) or not os.listdir(persistent_directory):
    print("First time running - creating vector store...")
    all_docs = []

    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        docs = loader.load()
        all_docs.extend(docs)
    #print(all_docs)
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
    docs = text_splitter.split_documents(all_docs)
        
    print(f"Total chunks created: {len(docs)}")
    
    client = chromadb.PersistentClient(path=persistent_directory)
    
       
    db = Chroma.from_documents(
            docs,
            embeddings,
            client=client,                
            collection_name="odyssey"    
        )
# else :    
#     client = chromadb.PersistentClient(path=persistent_directory)

#     db = Chroma(
#         client=client,               
#         collection_name="odyssey",    
#         embedding_function=embeddings
#     )

# retriever = db.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={"k": 5, "score_threshold": 0.38}, #the more threshold
#     #the more super close
#  )
# full_chain =prompt_template|llm|StrOutputParser()
# while True:
#     user_input = input("your question?:")
#     if user_input == "a":
#         break
#     related_chunks = retriever.invoke(user_input)
#     answer = full_chain.invoke({
#         "question":user_input,
#         "related_chunks":related_chunks
#     })
#     print(answer)
    
    

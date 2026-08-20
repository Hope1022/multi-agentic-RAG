import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
#from llm import groq_llm as llm
from llm import llm

load_dotenv()
# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model="llama-3.3-70b-versatile"
# )

SUPERVISOR_SYSTEM_PROMPT = """You are a coordinator for a student study assistant.

You have 4 specialists:
PERFORMANCE: accesses quiz scores, attendance, homework from database
CURRICULUM: accesses course syllabus, study guides, past exams as PDFs
RESOURCE: accesses internet search for learning materials
STUDY_PLAN: accesses internet search for study strategies

First call — delegate by writing 4 specific instructions:
PERFORMANCE: specific instruction including student's subject and problem
CURRICULUM: specific instruction including what to look for in documents
RESOURCE: specific instruction including subject and specific weak topics
STUDY_PLAN: specific instruction including subject, score, and time until exam

Second call — synthesize 4 reports into final answer using this format:
WHY YOU STRUGGLED: one sentence using performance data
WHAT TO FOCUS ON: one sentence using curriculum data
BEST RESOURCES: two specific resources from resource report
YOUR PLAN: week 1, week 2, week 3 each in one line
PREDICTED OUTCOME: one sentence

Rules:
- first call: only write the 4 instructions, nothing else
- second call: only write the final answer, nothing else
- never make up information not in the reports
- keep total response under 200 words
- never ask a question"""


def supervisor_node(state):
    question = state["question"]

    performance = state.get("performance_result", "")
    curriculum  = state.get("curriculum_result", "")
    resource    = state.get("resource_result", "")
    study_plan  = state.get("study_plan_result", "")

    
    if performance and curriculum and resource and study_plan:
        prompt = f"""Student question: {question}

Performance report: {performance}

Curriculum report: {curriculum}

Resource report: {resource}

Study plan report: {study_plan}

Write the final personalized answer for the student."""

    
    else:
        prompt = f"Student question: {question}\n\nWrite the 4 investigation instructions."

    response = llm.invoke([
        SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])

    
    if not performance:
        return {"supervisor_instructions": response.content}

    
    return {"draft_answer": response.content}
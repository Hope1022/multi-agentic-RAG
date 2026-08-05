import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from database import get_connection
from dotenv import load_dotenv
from llm import groq_llm as llm
import asyncpg
import asyncio

load_dotenv()
DB_URL = os.getenv("DB_URL")

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model="llama-3.3-70b-versatile"
# )

PERFORMANCE_SYSTEM_PROMPT = """You are a student performance analyst.
Analyze the given academic data only.
Return findings in this exact format:

ROOT CAUSE: one sentence
WEAKEST TOPIC: one sentence  
SCORE TREND: one sentence
ATTENDANCE IMPACT: one sentence

Be specific with numbers. Max 4 lines total."""


async def get_student_data(student_id: int) -> str:
    conn = await asyncpg.connect(DB_URL)
    

    scores = await conn.fetch("""
        SELECT
            a.title,
            a.type,
            a.max_score,
            s.score,
            s.submitted,
            c.name as course_name,
            c.code as course_code
        FROM scores s
        JOIN assessments a ON s.assessment_id = a.id
        JOIN courses c ON a.course_id = c.id
        WHERE s.student_id = $1
        ORDER BY c.code, a.date
    """, student_id)
    # $1 → asyncpg uses $1 $2 not %s

    attendance = await conn.fetch("""
        SELECT
            c.code,
            c.name,
            at.date,
            at.present
        FROM attendance at
        JOIN courses c ON at.course_id = c.id
        WHERE at.student_id = $1
        ORDER BY c.code, at.date
    """, student_id)

    await conn.close()

    scores_text = "SCORES:\n"
    for row in scores:
        percentage = round((row["score"] / row["max_score"]) * 100) if row["submitted"] else 0
        scores_text += f"{row['course_code']} {row['title']} ({row['type']}): {row['score']}/{row['max_score']} = {percentage}%"
        if not row["submitted"]:
            scores_text += " NOT SUBMITTED"
        scores_text += "\n"

    attendance_text = "\nATTENDANCE:\n"
    for row in attendance:
        status = "present" if row["present"] else "ABSENT"
        attendance_text += f"{row['code']} {row['date']}: {status}\n"

    return scores_text + attendance_text

def parse_instruction(instructions: str, agent: str) -> str:
    for line in instructions.split("\n"):
        if line.startswith(f"{agent}:"):
            return line.replace(f"{agent}:", "").strip()
    return instructions
def performance_node(state):
    student_id   = state["student_id"]
    question     = state["question"]
    instructions = parse_instruction(state["supervisor_instructions"],"PERFORMANCE")
    raw_data = asyncio.run(get_student_data(student_id))

    prompt = f"""Student question: {question}

Your specific task: {instructions}

Raw student data from database:
{raw_data}

Analyze this data and return your findings."""

    response = llm.invoke([
        SystemMessage(content=PERFORMANCE_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])

    return {"performance_result": response.content}

# query = "I failed my calculus midterm. What do I do?"
# state = {
#     "question":query,
#     "student_id":1,
#     "supervisor_instructions":"PERFORMANCE: find scores and attendance CURRICULUM: find final exam topics RESOURCE: find integration tutorials STUDY_PLAN: find 3 week recovery plan"
    
# }
# result = performance_node(state)
# print(result)
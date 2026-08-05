import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

JUDGE_SYSTEM_PROMPT = """You are a quality control judge for an AI student assistant.
You receive a draft answer and the source data it was based on.
Your job is to check:

1. GROUNDING: is every claim backed by the source data?
2. HALLUCINATION: is anything made up or assumed?
3. RELEVANCE: does it actually answer the student's question?
4. TONE: is it appropriate and encouraging for a struggling student?

Respond in this exact format:

VERDICT: PASS or FAIL
REASON: one sentence explaining why
FIX: if FAIL, one sentence on what to fix. if PASS write NONE."""


def judge_node(state):
    question         = state["question"]
    draft            = state["draft_answer"]
    performance      = state.get("performance_result", "")
    curriculum       = state.get("curriculum_result", "")
    resource         = state.get("resource_result", "")
    study_plan       = state.get("study_plan_result", "")
    retry_count      = state.get("retry_count", 0)

    prompt = f"""Student question: {question}

SOURCE DATA:
Performance: {performance}
Curriculum: {curriculum}
Resources: {resource}
Study plan: {study_plan}

DRAFT ANSWER TO JUDGE:
{draft}

Check if every claim in the draft is backed by the source data above."""

    response = llm.invoke([
        SystemMessage(content=JUDGE_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])

    result = response.content
    if "VERDICT: PASS" in result:
        return {
            "final_answer": draft,
            "judge_feedback": result,
            "retry_count": retry_count
        }

    return {
        "final_answer": "",
        "judge_feedback": result,
        "retry_count": retry_count + 1
    }
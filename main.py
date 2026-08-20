import os
from dotenv import load_dotenv
from graph.graph import graph

load_dotenv()

def run():
    question   = input("Ask your study assistant: ")
    student_id = int(os.getenv("CURRENT_STUDENT_ID", 1))

    result = graph.invoke({
        "question":                question,
        "student_id":              student_id,
        "supervisor_instructions": "",
        "performance_result":      "",
        "curriculum_result":       "",
        "resource_result":         "",
        "study_plan_result":       "",
        "draft_answer":            "",
        "judge_feedback":          "",
        "final_answer":            "",
        "retry_count":             0
    })

    print("\n" + "="*60)
    print("STUDY ASSISTANT RESPONSE")
    print("="*60)
    print(result["draft_answer"])
    print("="*60)

    # if "VERDICT: FAIL" in result.get("judge_feedback", ""):
    #     print("\n[Note: answer was revised by quality judge]")

if __name__ == "__main__":
    run()
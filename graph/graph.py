import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from agents.supervisor import supervisor_node
from graph.synthesize import synthesize_node
from agents.performance import performance_node
from agents.curriculum import curriculum_node
from agents.resource import resource_node
from agents.study_plan import study_plan_node
from agents.judge import judge_node

load_dotenv()


class StudentState(TypedDict):
    question:                str
    student_id:              int
    supervisor_instructions: str
    performance_result:      str
    curriculum_result:       str
    resource_result:         str
    study_plan_result:       str
    draft_answer:            str
    judge_feedback:          str
    final_answer:            str
    retry_count:             int


def should_retry(state: StudentState) -> str:
    if state["final_answer"]:
        return "end"
    if state["retry_count"] >= 2:
        return "end"
    return "retry"


def force_final(state: StudentState) -> dict:
    if not state["final_answer"]:
        return {"final_answer": state["draft_answer"]}
    return {}


graph_builder = StateGraph(StudentState)

graph_builder.add_node("supervisor",  supervisor_node)
graph_builder.add_node("synthesize",  synthesize_node)
graph_builder.add_node("performance", performance_node)
graph_builder.add_node("curriculum",  curriculum_node)
graph_builder.add_node("resource",    resource_node)
graph_builder.add_node("study_plan",  study_plan_node)
#graph_builder.add_node("judge",       judge_node)
#graph_builder.add_node("force_final", force_final)
def route_supervisor(state):
    if state["draft_answer"]:
        return END
    return ["performance", "curriculum", "resource", "study_plan"]

graph_builder.add_edge(START, "supervisor")
graph_builder.add_conditional_edges("supervisor", route_supervisor)
graph_builder.add_edge("performance", "synthesize")
graph_builder.add_edge("curriculum",  "synthesize")
graph_builder.add_edge("resource",    "synthesize")
graph_builder.add_edge("study_plan",  "synthesize")

graph_builder.add_edge("synthesize", "supervisor")

# supervisor → judge
# graph_builder.add_edge("supervisor",  "judge")

# graph_builder.add_conditional_edges(
#     "judge",
#     should_retry,
#     {
#         "end":   "force_final",
#         "retry": "supervisor"
#     }
# )

#graph_builder.add_edge("force_final", END)

# graph_builder.add_edge("supervisor", END)

graph = graph_builder.compile()
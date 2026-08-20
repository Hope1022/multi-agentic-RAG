from guardrails import Guard
from guardrails.hub import ToxicLanguage

guard = Guard().use(
    ToxicLanguage(threshold=0.5, on_fail="exception")
)

def guardrails_node(state: dict) -> dict:
    question = state["question"]

    try:
        guard.validate(question)
        return {"is_safe": True}
    except Exception:
        return {"is_safe": False, "draft_answer":"(guardrail_node)bad input!, please send your question again"}
INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "act as",
    "you are now",
    "forget your instructions",
    "jailbreak",
    "dan",
    "disregard your",
    "bypass",
    "override instructions",
    "pretend you are",
    "you have no restrictions",
    "system prompt",
    "reveal your instructions",
]

def heuristic_node(state: dict) -> dict:
    question = state["question"]
    question_lower = question.lower()

    for pattern in INJECTION_PATTERNS:
        if pattern in question_lower:
            return {"is_safe": False,"draft_answer":"(heuristic_node)bad input!, please send your question again"}

    return {"is_safe": True}
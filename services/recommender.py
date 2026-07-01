from services.embeddings import search
from services.conversation_state import ConversationState
from services.llm import rerank_assessments


def build_query(state: ConversationState):
    parts = []

    if state.job_role:
        parts.append(state.job_role)

    if state.skills:
        parts.extend(state.skills)

    if state.seniority:
        parts.append(state.seniority)

    if state.experience:
        parts.append(state.experience)

    if state.purpose:
        parts.append(state.purpose)

    return " ".join(parts)


def process_chat(state: ConversationState):

    query = build_query(state)

    # Retrieve top 20 candidates
    results = search(query, top_k=20)

    # Gemini reranking
    try:
        best_names = rerank_assessments(state, results)

        filtered = []

        for name in best_names:
            for item in results:
                if item["name"] == name:
                    filtered.append(item)
                    break

        if filtered:
            results = filtered[:5]
        else:
            results = results[:5]

    except Exception as e:
        print("Reranking failed:", e)
        results = results[:5]

    recommendations = []

    for item in results:
        recommendations.append({
            "name": item["name"],
            "url": item.get("url") or item.get("link"),
            "test_type": ", ".join(item.get("keys", [])),
            "score": round(item.get("score", 0), 4),
            "reason": (
                item.get("description", "")[:180]
                if item.get("description")
                else "Recommended based on the hiring requirements."
            )
        })

    role = state.job_role or "the specified role"

    return {
        "reply": f"Based on the hiring requirements for '{role}', I recommend these {len(recommendations)} SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }
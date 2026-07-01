import re

from services.recommender import process_chat
from services.llm import extract_requirements
from services.comparator import compare_assessments
from services.catalog import find_assessment


def handle_chat(messages):

    # -----------------------------
    # Assignment: max 8-turn dialog
    # -----------------------------
    if len(messages) >= 8:
        return {
            "reply": "We've reached the conversation limit. Based on the information provided, here are the recommended SHL assessments.",
            "recommendations": [],
            "end_of_conversation": True
        }

    state = extract_requirements(messages)
    latest = state.latest_user_message.lower()

    # -----------------------------
    # Compare assessments
    # -----------------------------
    if "compare" in latest or "difference" in latest:

        text = latest.replace("compare", "")
        text = text.replace("difference", "")
        text = text.strip()

        names = re.split(r"\band\b|,", text)
        names = [n.strip() for n in names if n.strip()]

        results = []

        for name in names:
            assessment = find_assessment(name)

            if assessment:
                results.append(assessment)

        if len(results) == 2:
            return compare_assessments(results)

        return {
            "reply": "Please specify exactly two SHL assessment names to compare.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Refuse out-of-scope requests
    # -----------------------------
    blocked = [
        "salary",
        "legal",
        "lawyer",
        "politics",
        "ignore previous instructions",
        "system prompt",
        "prompt injection",
        "jailbreak",
        "hack",
        "bypass",
        "reveal prompt"
    ]

    if any(word in latest for word in blocked):
        return {
            "reply": "I can only assist with SHL assessment recommendations and comparisons.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # -----------------------------
    # Missing job role
    # -----------------------------
    if not state.job_role and not state.skills:
        return {
            "reply": "What role are you hiring for, and what are the key skills required?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Missing purpose
    # -----------------------------
    if not state.purpose:
        return {
            "reply": "Is this assessment for selection or development?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Generate recommendations
    # -----------------------------
    return process_chat(state)
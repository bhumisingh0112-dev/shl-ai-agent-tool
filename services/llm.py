import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

from services.conversation_state import (
    ConversationState,
    extract_state
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_requirements(messages):
    """
    Extract hiring requirements using Gemini.
    Falls back to regex extraction if Gemini fails.
    """

    try:

        conversation = "\n".join(
            f"{m.role}: {m.content}"
            for m in messages
        )

        prompt = f"""
You are an expert SHL hiring assistant.

Extract the hiring requirements from the conversation.

Return ONLY valid JSON.

Schema:

{{
    "job_role": "",
    "skills": [],
    "experience": "",
    "purpose": "",
    "seniority": ""
}}

Rules:
- job_role should be concise.
- skills must be a JSON array.
- purpose should be either "Selection" or "Development" if available.
- Return JSON only.
- Never return markdown.

Conversation:

{conversation}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        data = json.loads(text)

        state = ConversationState()

        state.job_role = data.get("job_role") or None
        state.skills = data.get("skills", [])
        state.experience = data.get("experience") or None
        state.purpose = data.get("purpose") or None
        state.seniority = data.get("seniority") or None
        state.latest_user_message = messages[-1].content.lower()

        return state

    except Exception as e:

        print("Gemini extraction failed:", e)

        return extract_state(messages)


def rerank_assessments(state, assessments):

    prompt = f"""
You are an SHL assessment expert.

Role: {state.job_role}
Skills: {", ".join(state.skills)}
Experience: {state.experience}
Purpose: {state.purpose}
Seniority: {state.seniority}

Return ONLY a JSON array containing the BEST 5 assessment names.

Assessments:

{json.dumps([
    {
        "name": a["name"],
        "description": a.get("description", ""),
        "keys": a.get("keys", [])
    }
    for a in assessments
], indent=2)}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        return json.loads(text)

    except ServerError:

        print("Gemini unavailable. Using FAISS ranking.")

        return [a["name"] for a in assessments[:5]]

    except Exception as e:

        print("Gemini rerank failed:", e)

        return [a["name"] for a in assessments[:5]]
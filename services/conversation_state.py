from dataclasses import dataclass, field
import re


@dataclass
class ConversationState:
    job_role: str | None = None
    seniority: str | None = None
    experience: str | None = None
    purpose: str | None = None

    skills: list[str] = field(default_factory=list)
    assessment_types: list[str] = field(default_factory=list)
    job_levels: list[str] = field(default_factory=list)

    latest_user_message: str = ""


def extract_state(messages):

    state = ConversationState()

    user_text = " ".join(
        msg.content.lower()
        for msg in messages
        if msg.role == "user"
    )

    state.latest_user_message = user_text

    experience_patterns = [
        r"\d+\+?\s*years",
        r"\d+\s*yrs",
        r"\d+\s*year"
    ]

    for pattern in experience_patterns:
        match = re.search(pattern, user_text)

        if match:
            state.experience = match.group()
            break

    levels = [
        "graduate",
        "entry-level",
        "mid-professional",
        "manager",
        "director",
        "executive",
        "supervisor",
        "cxo"
    ]

    for level in levels:
        if level in user_text:
            state.job_levels.append(level)

    if "selection" in user_text:
        state.purpose = "selection"
    elif "development" in user_text:
        state.purpose = "development"

    skills = [
        "java",
        "python",
        "backend",
        "frontend",
        "leadership",
        "communication",
        "reasoning",
        "numerical"
    ]

    for skill in skills:
        if skill in user_text:
            state.skills.append(skill)
            
    # print("LATEST:", state.latest_user_message)
    # print("JOB ROLE:", state.job_role)
    # print("SKILLS:", state.skills)
    # print("PURPOSE:", state.purpose)

    roles = [
    "developer",
    "engineer",
    "manager",
    "analyst",
    "administrator",
    "architect",
    "consultant",
    "designer",
    "tester"
    ]

    for role in roles:
        if role in user_text:
            state.job_role = role
            break

    return state
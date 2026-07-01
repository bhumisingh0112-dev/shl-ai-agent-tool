import re
from pathlib import Path


def load_conversation(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_all_conversations(folder="tests/conversations"):
    folder = Path(folder)

    conversations = {}

    for file in sorted(folder.glob("*.md")):
        conversations[file.stem] = load_conversation(file)

    return conversations


def parse_messages(markdown):
    """
    Convert SHL markdown conversation into API messages.
    """

    messages = []

    user_pattern = r"\*\*User\*\*\s*> (.*?)(?=\n\n\*\*Agent\*\*)"
    agent_pattern = r"\*\*Agent\*\*\s*(.*?)(?=\n\n_|### Turn|\Z)"

    users = re.findall(user_pattern, markdown, re.S)
    agents = re.findall(agent_pattern, markdown, re.S)

    for i in range(max(len(users), len(agents))):

        if i < len(users):
            messages.append({
                "role": "user",
                "content": users[i].strip()
            })

        if i < len(agents):
            reply = agents[i].strip()

            reply = re.sub(r"_.*", "", reply, flags=re.S).strip()

            messages.append({
                "role": "assistant",
                "content": reply
            })

    return messages
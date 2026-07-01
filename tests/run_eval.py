import os
import re

from models.schemas import Message
from services.agent import handle_chat

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET = os.path.join(BASE_DIR, "tests", "conversations")


def parse_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    pattern = r"\*\*(User|Agent)\*\*\s*> (.+?)(?=\n###|\n\*\*User|\n\*\*Agent|\Z)"

    turns = []

    for role, content in re.findall(pattern, text, flags=re.S):
        turns.append({
            "role": role.lower(),
            "content": content.strip()
        })

    return turns


for filename in sorted(os.listdir(DATASET)):

    if not filename.endswith(".md"):
        continue

    print("\n" + "=" * 80)
    print(filename)
    print("=" * 80)

    history = []

    for turn in parse_markdown(os.path.join(DATASET, filename)):

        if turn["role"] == "user":

            history.append(
                Message(
                    role="user",
                    content=turn["content"]
                )
            )

            response = handle_chat(history)

            print("\nUSER:")
            print(turn["content"])

            print("\nYOUR BOT:")
            print(response["reply"])

            if response["recommendations"]:
                print("\nRecommendations:")
                for r in response["recommendations"]:
                    print("-", r["name"])

        else:
            history.append(
                Message(
                    role="assistant",
                    content=turn["content"]
                )
            )
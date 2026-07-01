from utils import (
    load_all_conversations,
    parse_messages
)

conversations = load_all_conversations()

for name, text in conversations.items():

    print("=" * 70)
    print(name)
    print("=" * 70)

    messages = parse_messages(text)

    for msg in messages:
        print(msg)

    print()
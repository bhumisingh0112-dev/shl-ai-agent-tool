from services.conversation_state import extract_state
from models.schemas import Message

messages = [
    Message(
        role="user",
        content="We are hiring a Java backend engineer with 10 years experience for leadership selection."
    )
]

state = extract_state(messages)

print(state)
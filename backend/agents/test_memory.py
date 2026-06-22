from backend.agents.memory import memory

memory.add_messages(
    "user1",
    [
        "Hello",
        "How are you?"
    ]
)

print(
    memory.get_history(
        "user1"
    )
)
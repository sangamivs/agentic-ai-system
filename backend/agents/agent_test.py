from backend.agents.react_agent import run_agent

test_cases = [
    "What is your return policy?",
    "My order #9999 has not arrived, please help",
    "I want a refund for a broken product and the policy does not cover it"
]

for query in test_cases:

    print("\n" + "=" * 50)
    print(f"Q: {query}")

    result = run_agent(query)

    print(f"\nA: {result}")

    print("\n=== Multi-turn memory test ===")

run_agent(
    "Hi, my name is Sangami",
    "session_001"
)

result = run_agent(
    "What did I just tell you my name was?",
    "session_001"
)

print(result)
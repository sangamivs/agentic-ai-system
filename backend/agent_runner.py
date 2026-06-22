from agents.tools import (
    search_knowledge_base,
    check_order_status,
    escalate_ticket
)

tools = [
    search_knowledge_base,
    check_order_status,
    escalate_ticket
]

print("\nLoaded Tools:\n")

for tool in tools:
    print(f"Name: {tool.name}")
    print(f"Description: {tool.description}")
    print("-" * 50)
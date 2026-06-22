from agents.tools import (
    search_knowledge_base,
    check_order_status,
    escalate_to_human
)

print(
    search_knowledge_base.invoke(
        {"query": "refund policy"}
    )
)

print(
    check_order_status.invoke(
        {"order_id": "12345"}
    )
)

print(
    escalate_to_human.invoke(
        {
            "reason": "damaged product",
            "customer_message":
            "My package arrived broken"
        }
    )
)
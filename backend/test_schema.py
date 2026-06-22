from agents.schemas import (
    AgentResponse,
    ToolCall
)

response = AgentResponse(
    answer="Order shipped.",
    confidence=0.92,
    sources=["order_db"],
    needs_escalation=False,
    action_taken="check_order"
)

print(response.model_dump())

print("\n")

tool = ToolCall(
    tool_name="check_order",
    tool_input={
        "order_id": "12345"
    },
    reasoning="Customer asked for order status."
)

print(tool.model_dump())
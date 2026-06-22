from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

AGENT_SYSTEM = """
You are a helpful customer support agent for AcmeCorp.

You have access to these tools:

- search_knowledge_base:
  Use for product information,
  policies, FAQs, documentation.

- check_order_status:
  Use for order tracking.
  Requires an order ID.

- escalate_to_human:
  Use for complex complaints,
  damaged products,
  refund disputes,
  or situations requiring human review.

Always think step by step before responding.

If you are unsure,
escalate rather than guessing.
"""

agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", AGENT_SYSTEM),

        MessagesPlaceholder(
            variable_name="chat_history"
        ),

        ("human", "{input}"),

        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        ),
    ]
)
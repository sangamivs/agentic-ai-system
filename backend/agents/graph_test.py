from backend.agents.graph_agent import agent_graph
from langchain_core.messages import HumanMessage

config = {
    "configurable": {
        "thread_id": "test-session-1"
    }
}

for user_input in [
    "What is your return policy?",
    "How long does shipping take?",
    "My order #777 has not arrived"
]:

    result = agent_graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "session_id": "test-1"
        },
        config=config
    )

    last_msg = result["messages"][-1]

    print(f"\nQ: {user_input}")
    print(f"A: {last_msg.content}\n")
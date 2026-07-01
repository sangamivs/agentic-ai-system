from langchain_ollama import ChatOllama

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
    SystemMessage
)

from backend.agents.tools import (
    search_knowledge_base,
    check_order_status,
    escalate_to_human
)

AGENT_SYSTEM = """
You are AcmeCorp's customer support AI.

You have access to tools.

Rules:
- For ALL questions about returns, refunds, shipping, products or policies,
  ALWAYS call search_knowledge_base FIRST.
- Never answer these questions from memory.
- Use ONLY the retrieved information.
- If the knowledge base conflicts with your own knowledge,
  the knowledge base is ALWAYS correct.
- Never invent company policies.
"""

tools = [
    search_knowledge_base,
    check_order_status,
    escalate_to_human
]

tool_map = {
    tool.name: tool
    for tool in tools
}


def run_agent(
    user_input: str,
    history=None
):

    if history is None:
        history = []

    llm = ChatOllama(
        model="llama3.2:latest",
        temperature=0
    ).bind_tools(tools)

    messages = [
        SystemMessage(content=AGENT_SYSTEM)
    ]

    messages.extend(history)

    messages.append(
        HumanMessage(content=user_input)
    )

    for i in range(5):

        print(
            f"\n===== LOOP {i+1} ====="
        )

        response = llm.invoke(
            messages
        )

        messages.append(response)

        print(
            "\nAI RESPONSE:"
        )

        print(response.content)

        if not response.tool_calls:

            return {
                "answer": response.content,
                "history": messages
            }

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call["args"]

            tool = tool_map[tool_name]

            tool_result = tool.invoke(
                tool_args
            )

            print(
                "\nTOOL RESULT:"
            )

            print(tool_result)

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )

    return {
        "answer":
        "Maximum iterations reached.",
        "history": messages
    }


if __name__ == "__main__":

    history = []

    while True:

        user_input = input(
            "\nYou: "
        )

        if user_input.lower() == "exit":
            break

        result = run_agent(
            user_input,
            history
        )

        history = result["history"]

        print(
            f"\nAgent: {result['answer']}"
        )
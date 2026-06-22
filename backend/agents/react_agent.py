from backend.agents.memory import memory
from langchain_ollama import ChatOllama

from backend.agents.tools import (
    search_knowledge_base,
    check_order_status,
    escalate_to_human
)

from backend.agents.react_prompt import (
    REACT_PROMPT
)

# ----------------------------
# MODEL
# ----------------------------

llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)

# ----------------------------
# TOOLS
# ----------------------------

TOOLS = {
    "search_knowledge_base": search_knowledge_base,
    "check_order_status": check_order_status,
    "escalate_to_human": escalate_to_human
}

# ----------------------------
# PARSER
# ----------------------------

def parse_response(text):

    parsed = {}

    for line in text.split("\n"):

        if ":" in line:

            key, value = line.split(
                ":",
                1
            )

            parsed[key.strip()] = value.strip()

    return parsed


# ----------------------------
# AGENT
# ----------------------------

def run_agent(
    user_question,
    session_id="default"
):

    history = memory.get_history(
        session_id
    )

    history_text = "\n".join(
        str(msg)
        for msg in history
    )

    prompt = REACT_PROMPT.format(
        history=history_text,
        question=user_question
    )

    for step in range(5):

        print(
            f"\n===== AGENT STEP {step+1} ====="
        )

        response = llm.invoke(prompt)

        output = response.content

        print(output)

        # FINAL ANSWER

        if "Final Answer:" in output:

            answer = output.split(
                "Final Answer:",
                1
            )[1].strip()

            memory.add_messages(
                session_id,
                [
                    f"User: {user_question}",
                    f"Assistant: {answer}"
                ]
            )

            memory.add_messages(
                session_id,
                [
                    f"User: {user_question}",
                    f"Assistant: {output}"
                ]
            )

            return answer

        # PARSE TOOL CALL

        parsed = parse_response(output)

        action = parsed.get("Action", "")

        action = (
            action.replace("\\_", "_")
            .replace("`", "")
            .strip()
        )
        action_input = (
            parsed.get("Action Input")
            or parsed.get("Input")
            or ""
        )

        if not action:

            conversation_history.append(
                f"User: {user_question}"
            )

            conversation_history.append(
                f"Assistant: {output}"
            )

            return output

        if action not in TOOLS:

            return (
                f"Unknown tool: {action}"
            )

        # EXECUTE TOOL

        tool = TOOLS[action]

        tool_result = tool.invoke(action_input)

        try:

            answer_prompt = f"""
            You are a customer support agent.

            User Question:
            {user_question}

            Tool Result:
            {tool_result}

            Use the tool result to answer the user.

            Format:

            Final Answer: your answer
            """

            response = llm.invoke(answer_prompt)

            return response.content

        except Exception as e:

            return (
                f"Tool execution error: {e}"
            )

        print(
            "\nObservation:"
        )

        print(tool_result)


    return (
        "Maximum reasoning steps reached."
    )


# ----------------------------
# CHAT LOOP
# ----------------------------

if __name__ == "__main__":

    print(
        "Customer Support Agent Started"
    )

    print(
        "Type 'exit' to quit\n"
    )

    while True:

        user_input = input(
            "You: "
        )

        if user_input.lower() == "exit":
            break

        answer = run_agent(
            user_input
        )

        print(
            f"\nAgent: {answer}\n"
        )
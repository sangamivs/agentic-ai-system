from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from langchain_ollama import ChatOllama
from backend.agents.fallback_chain import get_llm_with_fallback

from langchain_core.messages import (
    BaseMessage,
    SystemMessage
)

from typing import TypedDict, Annotated
import operator

from backend.agents.tools import (
    search_knowledge_base,
    check_order_status,
    escalate_to_human
)

from backend.agents.tool_calling_agent import (
    AGENT_SYSTEM
)


tools = [
    search_knowledge_base,
    check_order_status,
    escalate_to_human
]

llm = get_llm_with_fallback(tools)

critic_llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    session_id: str


def agent_node(state: AgentState):

    messages = [
        SystemMessage(content=AGENT_SYSTEM)
    ] + state["messages"]

    response = llm(messages)
    
    print("\n" + "=" * 50)
    print("TOKEN USAGE")
    print("=" * 50)

    if hasattr(response, "response_metadata"):

        metadata = response.response_metadata

        print("Raw metadata:")
        print(metadata)

        input_tokens = metadata.get("prompt_eval_count", 0)
        output_tokens = metadata.get("eval_count", 0)

        print(f"Input tokens: {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(f"Total tokens: {input_tokens + output_tokens}")

    else:
        print("No token metadata available")

    print("=" * 50)

    return {
        "messages": [response]
    }

def critic_node(state: AgentState):

    last_response = state["messages"][-1].content

    critique_prompt = f"""
Review this customer support response.

Response:
{last_response}

Check:
1. Is it factually grounded?
2. Is it helpful?
3. Any policy violations?

If good, output APPROVED.

If changes are needed output:
REVISE: reason
"""

    critique = critic_llm.invoke(critique_prompt)

    print("\nCRITIC REVIEW:")
    print(critique.content)

    if "REVISE" in critique.content:

        return {
            "messages": [
                HumanMessage(
                    content=f"""
Revise your response.

Feedback:
{critique.content}
"""
                )
            ]
        }

    return {
        "messages": []
    }

def should_continue(state: AgentState):

    last = state["messages"][-1]

    return "tools" if last.tool_calls else END

tool_node = ToolNode(tools)

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

workflow.add_edge(
    "tools",
    "agent"
)

agent_graph = workflow.compile(
    checkpointer=MemorySaver()
)
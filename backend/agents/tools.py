from langchain_core.tools import tool
from backend.rag.retriever import KnowledgeBaseRetriever

retriever = KnowledgeBaseRetriever()


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the product knowledge base for information.
    Use for product questions, refund policies,
    shipping policies, FAQs, and documentation.
    """

    results = retriever.retrieve(query)

    if not results:
        return "No relevant information found in the knowledge base."

    context = "\n\n---\n\n".join(results)

    return (
        f"Relevant information from knowledge base:\n\n"
        f"{context}"
    )


@tool
def check_order_status(order_id: str) -> str:
    """
    Check the status of a customer order using
    the order ID.
    """

    return (
        f"Order {order_id}: "
        f"Shipped on 2024-01-10, "
        f"expected delivery 2024-01-15"
    )


@tool
def escalate_to_human(reason: str) -> str:
    """
    Escalate a complex issue to a human
    support agent.
    """

    return (
        f"Ticket created. "
        f"A human agent will respond within "
        f"2 hours. Reason: {reason}"
    )
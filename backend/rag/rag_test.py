from backend.agents.tools import search_knowledge_base
from langchain_ollama import ChatOllama

question = "What is the return policy?"

# Retrieve context from RAG
context = search_knowledge_base.invoke(
    {"query": question}
)

print("\nRETRIEVED CONTEXT:\n")
print(context[:500])

# Generate answer using context
llm = ChatOllama(
    model="gemma3:1b",
    temperature=0
)

response = llm.invoke(
    f"""
    Context:
    {context}

    Question:
    {question}

    Answer only using the context provided.
    """
)

print("\nFINAL ANSWER:\n")
print(response.content)
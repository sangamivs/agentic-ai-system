from backend.agents.tools import search_knowledge_base

result = search_knowledge_base.invoke(
    {
        "query": "What is the return policy?"
    }
)

print(result)
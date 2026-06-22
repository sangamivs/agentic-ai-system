from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

from agents.schemas import AgentResponse

llm = Ollama(
    model="gemma3:1b",
    format="json"
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
IMPORTANT:
Return ONLY valid JSON.
No markdown.
No explanations.
No extra text.

JSON schema:
{schema}
"""
        ),
        (
            "human",
            "{query}"
        )
    ]
)

chain = prompt | llm

result = chain.invoke(
    {
        "schema": AgentResponse.model_json_schema(),
        "query": "Where is my order 12345?"
    }
)

print(result)
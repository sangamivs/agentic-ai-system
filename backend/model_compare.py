from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.1:8b")

response = llm.invoke(
    "You are a customer support agent. A customer says: My order has not arrived in 10 days. What should I do?"
)

print(response)
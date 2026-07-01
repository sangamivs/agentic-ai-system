from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
)

from datasets import Dataset
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# Local Ollama LLM
llm = LangchainLLMWrapper(
    ChatOllama(model="llama3.2:latest")
)

# Local Ollama Embeddings
embeddings = LangchainEmbeddingsWrapper(
    OllamaEmbeddings(model="nomic-embed-text:latest")
)

data = {
    "question": [
        "What is the return policy?",
        "How long does shipping take?"
    ],
    "answer": [
        "We offer a 30 day return policy with full refund.",
        "Standard shipping takes 3-5 business days."
    ],
    "contexts": [
        ["Return policy: Customers can return products within 30 days for a full refund."],
        ["Shipping information: Standard shipping takes 3-5 business days."]
    ],
    "ground_truth": [
        "30 day return policy with full refund",
        "3-5 business days standard shipping"
    ]
}

dataset = Dataset.from_dict(data)

result = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision
    ],
    llm=llm,
    embeddings=embeddings,
)

print(result)
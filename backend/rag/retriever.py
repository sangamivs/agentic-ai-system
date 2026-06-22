from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


class KnowledgeBaseRetriever:

    def __init__(
        self,
        persist_dir="data/chroma_db"
    ):

        embeddings = OllamaEmbeddings(
            model="nomic-embed-text"
        )

        self.vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )

        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 3,
                "fetch_k": 10
            }
        )

    def retrieve(self, query: str):

        docs = self.retriever.invoke(query)

        return [
            doc.page_content
            for doc in docs
        ]


if __name__ == "__main__":

    r = KnowledgeBaseRetriever()

    results = r.retrieve(
        "What is the return policy?"
    )

    for i, chunk in enumerate(results):
        print(f"\nChunk {i+1}")
        print("-" * 50)
        print(chunk[:200])
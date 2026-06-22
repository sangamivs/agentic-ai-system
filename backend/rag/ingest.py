from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


def ingest_documents(
    docs_dir="data/documents",
    persist_dir="data/chroma_db"
):

    loader = DirectoryLoader(
        docs_dir,
        glob="*.txt",
        loader_cls=TextLoader
    )

    docs = loader.load()

    print(f"Loaded {len(docs)} documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    print(f"Created {len(chunks)} chunks")

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    print(f"Stored in ChromaDB at {persist_dir}")

    return vectorstore


if __name__ == "__main__":
    ingest_documents()
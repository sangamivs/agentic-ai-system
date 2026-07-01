from fastapi import APIRouter
from backend.api.models import HealthResponse
import httpx

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    ollama_ok = False

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "http://localhost:11434/api/tags",
                timeout=3
            )
            ollama_ok = r.status_code == 200
    except:
        pass

    chroma_ok = False

    try:
        from backend.rag.retriever import KnowledgeBaseRetriever

        KnowledgeBaseRetriever()
        chroma_ok = True
    except:
        pass

    return HealthResponse(
        status="healthy" if ollama_ok else "degraded",
        ollama_connected=ollama_ok,
        chromadb_connected=chroma_ok
    )
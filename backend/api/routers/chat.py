from fastapi import APIRouter, HTTPException, WebSocket, Request
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from backend.api.output_filter import filter_output
from backend.api.limiter import limiter
from backend.api.models import ChatRequest, ChatResponse
from backend.api.guardrails import validate_input, validate_output
from backend.agents.graph_agent import agent_graph
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(request: Request, body: ChatRequest):
    try:
        message = validate_input(body.message)

        config = {
            "configurable": {
                "thread_id": body.session_id
            }
        }

        # Structured log
        logger.info("Agent invoked")

        result = agent_graph.invoke(
            {
                "messages": [
                    HumanMessage(content=message)
                ],
                "session_id": body.session_id
            },
            config=config
        )

        last = result["messages"][-1]

        tool_calls = sum(
            1
            for m in result["messages"]
            if hasattr(m, "tool_calls") and m.tool_calls
        )

        # Structured log
        logger.info(
            f"Request completed | session={body.session_id} | tools={tool_calls}"
        )

        print("LAST CONTENT:")
        print(last.content)
        print(type(last.content))

        filtered_answer = filter_output(
            validate_output(last.content)
        )

        return ChatResponse(
            answer=filtered_answer,
            session_id=body.session_id,
            tool_calls_made=tool_calls
        )

    except Exception as e:
        logger.exception("Chat endpoint failed")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.websocket("/ws/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    await websocket.accept()

    llm_stream = ChatOllama(
        model="llama3.2:latest",
        streaming=True
    )

    try:
        while True:
            user_msg = await websocket.receive_text()

            user_msg = validate_input(user_msg)

            logger.info(f"WebSocket message | session={session_id}")

            async for chunk in llm_stream.astream(user_msg):
                if chunk.content:
                    await websocket.send_text(chunk.content)

            await websocket.send_text("[DONE]")

    except HTTPException as e:
        logger.warning(f"Blocked input: {e.detail}")
        await websocket.send_text(f"ERROR: {e.detail}")

    except Exception as e:
        logger.exception("WebSocket Error")
        import traceback
        traceback.print_exc()
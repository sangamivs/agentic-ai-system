from pydantic import BaseModel, Field
from typing import Optional, Literal


class AgentResponse(BaseModel):
    answer: str = Field(
        description="The response to the user"
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    sources: list[str] = Field(
        default=[],
        description="Source docs used"
    )

    needs_escalation: bool = False

    action_taken: Optional[str] = None


class ToolCall(BaseModel):
    tool_name: Literal[
        "search_kb",
        "check_order",
        "escalate"
    ]

    tool_input: dict

    reasoning: str
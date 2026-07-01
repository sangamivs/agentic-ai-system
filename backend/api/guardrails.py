import re
from fastapi import HTTPException

INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior|above) instructions",
    r"you are now",
    r"disregard your",
    r"act as (a |an )?different",
    r"reveal (your |the )?system prompt",
]


def validate_input(text: str) -> str:
    print(f"\nReceived input: {text}")

    if len(text) > 2000:
        print("❌ Message too long")
        raise HTTPException(
            status_code=400,
            detail="Message too long (max 2000 chars)"
        )

    text_lower = text.lower()

    for pattern in INJECTION_PATTERNS:
        print(f"Checking pattern: {pattern}")

        if re.search(pattern, text_lower):
            print("🚨 Prompt injection detected!")
            raise HTTPException(
                status_code=400,
                detail="Message contains invalid content"
            )

    print("✅ Input validation passed")
    return text.strip()


def validate_output(text: str) -> str:
    if len(text) > 5000:
        print("⚠️ Output truncated")
        return text[:5000] + "... [truncated]"

    return text
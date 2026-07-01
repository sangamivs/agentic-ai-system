import re

COMPETITOR_NAMES = [
    "CompetitorA",
    "CompetitorB"
]


def filter_output(text: str, context: dict = None) -> str:
    # Hide competitor names
    for name in COMPETITOR_NAMES:
        text = re.sub(
            name,
            "[competitor]",
            text,
            flags=re.IGNORECASE
        )

    # Hide email addresses
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    emails = re.findall(email_pattern, text)

    for email in emails:
        text = text.replace(email, "[email redacted]")

    return text
"""Basic input validation for the local demo. This is not production authentication."""
def sanitize_input(value: str, max_length: int = 2000) -> str:
    if value is None:
        return ""
    return str(value).strip()[:max_length]

def validate_ticket_payload(category: str, subject: str, description: str) -> bool:
    return bool(category and subject and description and len(subject.strip()) <= 150 and len(description.strip()) <= 2000)

def validate_text(value: str, limit: int = 5000) -> bool:
    return bool(value and value.strip() and len(value.strip()) <= limit)

# utils.py
from fastapi.responses import PlainTextResponse
from datetime import datetime, timezone
from typing import Optional, Tuple
import re

def plain_text_response(msg: str, status_code: int = 200):
    # Twilio accepts plain text OK responses; TwiML is optional.
    return PlainTextResponse(content=msg, status_code=status_code)

def now_utc_iso():
    return datetime.now(timezone.utc).isoformat()

# Basic sanitizers & validators
def sanitize_text(s: Optional[str]) -> str:
    if s is None:
        return ""
    # collapse whitespace and trim
    return re.sub(r'\s+', ' ', s).strip()

def validate_lengths(product_name: str, user_name: str, review_text: str) -> Tuple[bool, str]:
    if not (1 <= len(product_name) <= 200):
        return False, "Product name must be 1-200 characters."
    if not (1 <= len(user_name) <= 100):
        return False, "User name must be 1-100 characters."
    if not (1 <= len(review_text) <= 5000):
        return False, "Review must be 1-5000 characters."
    return True, ""

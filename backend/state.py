# state.py
"""
Simple in-memory conversation state store.

Structure:
CONV_STATE = {
  "<contact_number>": {
      "state": "AWAIT_PRODUCT" | "AWAIT_NAME" | "AWAIT_REVIEW",
      "product_name": "...",
      "user_name": "...",
      "last_ts": 169... (epoch seconds)
  }
}

LIMITATION: This is ephemeral. If process restarts state is lost.
For production use Redis or DB-backed in_progress table.
"""
from time import time
import os

CONV_STATE: dict = {}
STATE_TTL_SECONDS = int(os.getenv("STATE_TTL_SECONDS", 1800))  # default 30 minutes

def get_state(contact: str):
    cleanup_expired()
    return CONV_STATE.get(contact)

def set_state(contact: str, state_obj: dict):
    state_obj["last_ts"] = int(time())
    CONV_STATE[contact] = state_obj

def clear_state(contact: str):
    if contact in CONV_STATE:
        del CONV_STATE[contact]

def cleanup_expired():
    now = int(time())
    expired = [k for k, v in CONV_STATE.items() if now - v.get("last_ts", 0) > STATE_TTL_SECONDS]
    for k in expired:
        del CONV_STATE[k]

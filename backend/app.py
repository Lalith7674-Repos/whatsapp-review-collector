# app.py
import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, Base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from models import Review
from schemas import ReviewOut
from state import get_state, set_state, clear_state, cleanup_expired
from utils import plain_text_response, sanitize_text, validate_lengths
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import List

load_dotenv()

# create DB tables (simple approach for assignment)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WhatsApp Review Collector (backend)")

# Basic CORS - allow local frontend during dev; adjust origin in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # narrow this down in real deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple idempotency check: detect duplicates within a short window by equality
def is_duplicate(db: Session, contact: str, product: str, review_text: str) -> bool:
    stmt = select(Review).where(
        Review.contact_number == contact,
        Review.product_name == product,
        Review.product_review == review_text
    ).order_by(Review.created_at.desc()).limit(1)
    res = db.execute(stmt).scalars().first()
    if not res:
        return False
    # if found record within last 10 minutes, treat as duplicate
    delta = datetime.now(timezone.utc) - res.created_at
    return delta.total_seconds() < 600  # 10 minutes

@app.post("/whatsapp")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Twilio will POST form-encoded data. We only need From and Body.
    From example: "whatsapp:+1415XXXXXXX"
    """
    form = await request.form()
    from_raw = form.get("From")
    body_raw = form.get("Body", "")
    if not from_raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing 'From' in request")
    contact = from_raw.replace("whatsapp:", "").strip()
    body = sanitize_text(body_raw)

    # clear expired states opportunistically
    cleanup_expired()

    # allow user to cancel mid-flow
    if body.lower() == "cancel":
        clear_state(contact)
        return plain_text_response("Conversation cancelled. Send any message to start again.")

    state = get_state(contact)
    if not state:
        # start new conversation
        set_state(contact, {"state": "AWAIT_PRODUCT"})
        return plain_text_response("Which product is this review for?")

    current_state = state.get("state")
    if current_state == "AWAIT_PRODUCT":
        # store product name and ask for user's name
        if not body:
            return plain_text_response("Please send the product name.")
        set_state(contact, {"state": "AWAIT_NAME", "product_name": body})
        return plain_text_response("What's your name?")

    if current_state == "AWAIT_NAME":
        if not body:
            return plain_text_response("Please send your name.")
        # store name and ask for review
        updated = {"state": "AWAIT_REVIEW", "product_name": state.get("product_name"), "user_name": body}
        set_state(contact, updated)
        return plain_text_response(f"Please send your review for {state.get('product_name')}.")

    if current_state == "AWAIT_REVIEW":
        if not body:
            return plain_text_response("Please send your review text.")
        product_name = state.get("product_name")
        user_name = state.get("user_name")
        review_text = body

        # basic validation
        ok, msg = validate_lengths(product_name, user_name, review_text)
        if not ok:
            # keep state intact so user can correct
            return plain_text_response(f"Validation error: {msg}")

        # idempotency / duplicate check
        try:
            if is_duplicate(db, contact, product_name, review_text):
                clear_state(contact)
                return plain_text_response("Duplicate review detected — we've already recorded this. Thank you.")
        except SQLAlchemyError:
            # don't block flow if DB check fails; continue to try insert
            pass

        # persist to DB
        try:
            new = Review(
                contact_number=contact,
                user_name=user_name,
                product_name=product_name,
                product_review=review_text,
                # created_at will be set by DB server_default (func.now()), but we can also set client-side:
                created_at=datetime.now(timezone.utc)
            )
            db.add(new)
            db.commit()
            db.refresh(new)
        except Exception as e:
            db.rollback()
            # log in real app; here return error message
            return plain_text_response("Failed to save your review. Please try again later.", status_code=500)

        clear_state(contact)
        return plain_text_response(f"Thanks {user_name} — your review for {product_name} has been recorded.")

    # fallback safety
    clear_state(contact)
    return plain_text_response("Sorry, something went wrong. Send any message to start again.")

@app.get("/api/reviews", response_model=List[ReviewOut])
def get_reviews(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    limit = min(1000, max(1, limit))
    offset = max(0, offset)
    stmt = select(Review).order_by(Review.created_at.desc()).limit(limit).offset(offset)
    rows = db.execute(stmt).scalars().all()
    return rows

@app.get("/health")
def health():
    return {"status": "ok"}

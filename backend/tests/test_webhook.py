# tests/test_webhook.py
import pytest
from fastapi.testclient import TestClient
import os
import sys
# ensure backend package import paths
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import app
from database import Base, engine, SessionLocal
from models import Review

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # create tables in test DB (uses same DB in .env by default)
    Base.metadata.create_all(bind=engine)
    # cleanup before/after
    yield
    # drop all reviews created during tests (simple cleanup)
    # Using SQLAlchemy 2.0 style delete
    with SessionLocal() as db:
        from sqlalchemy import delete
        db.execute(delete(Review))
        db.commit()

def post_whatsapp(from_number: str, body: str):
    return client.post("/whatsapp", data={"From": from_number, "Body": body})

def test_full_flow():
    from_num = "whatsapp:+15550001111"
    # start
    r = post_whatsapp(from_num, "Hello")
    assert r.status_code == 200 and "Which product" in r.text

    r = post_whatsapp(from_num, "Widget X")
    assert r.status_code == 200 and "What's your name" in r.text

    r = post_whatsapp(from_num, "Alice")
    assert r.status_code == 200 and "Please send your review for Widget X" in r.text

    r = post_whatsapp(from_num, "This product is great!")
    assert r.status_code == 200 and "your review for Widget X has been recorded" in r.text

    # check GET /api/reviews returns at least one item for the user
    r2 = client.get("/api/reviews")
    assert r2.status_code == 200
    data = r2.json()
    assert any(item["contact_number"].endswith("1111") and item["product_name"] == "Widget X" for item in data)

# Backend - WhatsApp Review Collector

FastAPI service that drives the WhatsApp conversation flow and persists reviews to PostgreSQL.

## Running

The backend runs automatically when you execute `docker compose up --build` from the repo root.
If you want to run it manually:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # populate credentials
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Expose port 8000 publicly (ngrok/Codespaces/Gitpod) and point Twilio’s sandbox webhook to
`https://<public-host>/whatsapp`.

## Endpoints

- `POST /whatsapp` : Twilio webhook (form-encoded). Required form fields: `From`, `Body`.
- `GET /api/reviews` : Returns JSON list of reviews (supports `limit` and `offset` query params).
- `GET /health` : Simple health check.

## Limitations & Notes

- Conversation state is stored in memory (`state.py`). If the process restarts, ongoing conversations are lost.
For production use, migrate state to Redis or a DB-backed `in_progress_reviews` table.
- The code contains a simple duplicate protection (checks identical contact/product/review within 10 minutes).
- Twilio signature validation is not implemented here. If you expose publicly, implement request signature validation.
- CORS is permissive (`allow_origins=["*"]`) for local dev; lock this down in production.

## Tests

```bash
cd backend
pytest -q
```

## Future improvements

- Replace in-memory state with Redis for reliability.
- Add authentication or admin UI as needed.
- Add structured logging and monitoring.

# Backend - WhatsApp Review Collector

This backend is a minimal FastAPI service that receives WhatsApp messages via Twilio webhook,
runs a small conversation flow to collect: product name, user name, review text, and stores reviews
in Postgres.

## Quick start (local)

1. Create Python virtualenv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure Postgres:
- Use Docker Compose (recommended) or local Postgres.
- Example Docker Compose (root `docker-compose.yml`):
  ```yaml
  services:
    db:
      image: postgres:14
      environment:
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: postgres
        POSTGRES_DB: reviewsdb
      ports:
        - "5432:5432"
  ```

3. Create `.env` from `.env.example` and set `DATABASE_URL`.

4. Run the app:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

5. Expose to Twilio using `ngrok`:

```bash
ngrok http 8000
```

Set Twilio sandbox "WHEN A MESSAGE COMES IN" webhook to:
`https://<ngrok-id>.ngrok.io/whatsapp`

6. Use Twilio WhatsApp sandbox to send messages and test.

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

Run tests with:

```bash
pytest -q
```

(Tests use the DB configured via `DATABASE_URL` — they will insert and then delete review rows.)

## Next steps

- Replace in-memory state with Redis for reliability.
- Add authentication or admin UI as needed.
- Add structured logging and monitoring.

# WhatsApp Product Review Collector

Collect reviews via WhatsApp → FastAPI saves them to PostgreSQL → React frontend displays them.  
Stack: FastAPI · PostgreSQL · React (Vite) · Twilio Sandbox · Docker Compose

---

## 1. Launch in GitHub Codespaces (recommended)

1. Open the repo on GitHub → **Code** → **Codespaces** → *Create codespace on main*.  
2. Wait for VS Code (browser) to start.  
3. In the terminal run:
   ```bash
   docker compose up --build
   ```
4. Open the **Ports** tab. For port **8000** click the lock (make it **Public**) and open the globe icon; do the same for port **3000** (frontend).

> Running locally? Install Docker Desktop and run the same command. URLs become http://localhost:8000 and http://localhost:3000.

Stop everything with `Ctrl+C` or `docker compose down`.

---

## 2. Environment variables

Copy `backend/.env.example` → `backend/.env` and fill in:
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/reviewsdb
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
APP_HOST=0.0.0.0
APP_PORT=8000
STATE_TTL_SECONDS=1800
```
No ngrok values are required.

---

## 3. Twilio Sandbox setup (step-by-step)

1. **Join sandbox from your phone**  
   - Twilio Console → Messaging → *Send a WhatsApp message*.  
   - Send the displayed join code (e.g., `join strip-image`) to `+1 415 523 8886`.

2. **Verify backend URL**  
   - Use the public port-8000 URL from Codespaces.  
   - Visit `https://<port-8000-url>/health` → expect `{"status":"ok"}`.

3. **Configure webhook**  
   - Twilio Console → *Sandbox settings*.  
   - Set **When a message comes in** to `https://<port-8000-url>/whatsapp`.  
   - Method: `POST`. Click **Save**.

4. **Send a WhatsApp message**  
   - Send `hi` to the sandbox number.  
   - Provide product name → user name → review.

5. **View the review**  
   - Open the public port-3000 URL (frontend).  
   - The review appears in the table once the flow finishes.

> Every time the Codespace restarts, the port URL changes—update Twilio with the new `<url>/whatsapp`.

---

## 4. Testing & useful commands

```bash
cd backend && pytest -q        # unit tests
curl http://localhost:8000/health
curl http://localhost:8000/api/reviews

curl -X POST http://localhost:8000/whatsapp \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hi"
```

Docker helpers:
```bash
docker compose up --build
docker compose down
docker compose logs backend
docker exec -it whatsapp-review-db psql -U postgres -d reviewsdb
```

---

## 5. Project structure

```
whatsapp-review-collector/
├── backend/      # FastAPI app (Dockerfile, tests, env example)
├── frontend/     # React app served by Nginx (Dockerfile, Vite)
├── docker-compose.yml
└── README.md
```

### API overview
| Method | Path           | Description                     |
|--------|----------------|---------------------------------|
| POST   | `/whatsapp`    | Twilio webhook (form data)      |
| GET    | `/api/reviews` | List stored reviews (JSON)      |
| GET    | `/health`      | Health check                    |

---

## 6. Known limitations

1. Conversation state is stored in memory—restart wipes in-progress flows.
2. Twilio Sandbox requires every tester to join with the sandbox code before messaging.
3. Codespaces/ngrok URLs change after restarts; remember to update the webhook.
4. CORS is wide-open for local dev; tighten before production.
5. Twilio signature validation isn’t implemented (add for production).

Need more detail? Check `/backend/README-backend.md` and `/frontend/README-frontend.md`.  
Happy building! 🚀

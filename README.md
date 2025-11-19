# WhatsApp Product Review Collector

A full-stack application that collects product reviews via WhatsApp using Twilio, stores them in PostgreSQL, and displays them in a React frontend.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Complete Setup Guide](#complete-setup-guide)
- [Environment Variables](#environment-variables)
- [Twilio WhatsApp Setup](#twilio-whatsapp-setup)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Troubleshooting](#troubleshooting)
- [Known Limitations](#known-limitations)

---

## Project Overview

This project implements a WhatsApp Product Review Collector using:
- **FastAPI** (Python backend)
- **PostgreSQL** (database)
- **React** (frontend)
- **Twilio** (WhatsApp integration)

**How it works:**
1. Users send WhatsApp messages to Twilio sandbox number
2. Messages arrive at `/whatsapp` webhook endpoint
3. Backend follows conversational flow to collect: product name, user name, review text
4. Reviews stored in PostgreSQL
5. Frontend displays reviews via `/api/reviews` endpoint

---

## Quick Start

### Prerequisites

- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop)
- **Twilio Account** - [Sign up](https://www.twilio.com/try-twilio)
- **ngrok** - [Download](https://ngrok.com/download) (for webhook tunneling)

### 5-Minute Setup

1. **Install Docker Desktop** and restart your computer

2. **Start all services:**
   ```bash
   docker-compose up --build
   ```

3. **Access your application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Set up Twilio** (see [Twilio WhatsApp Setup](#twilio-whatsapp-setup) below)

5. **Test it!** Send a WhatsApp message to your sandbox number

---

## Complete Setup Guide

### Step 1: Install Docker Desktop

1. Download from: https://www.docker.com/products/docker-desktop
2. Install and restart your computer
3. Verify Docker is running (Docker icon in system tray)

### Step 2: Start All Services

```bash
docker-compose up --build
```

**What happens:**
- ✅ Downloads PostgreSQL (first time only)
- ✅ Starts PostgreSQL database
- ✅ Builds and starts FastAPI backend
- ✅ Builds React frontend and serves it with Nginx

**Wait 1-2 minutes** for everything to build and start.

**Verify services are running:**
```bash
docker ps
```

You should see 3 containers:
- `whatsapp-review-db` (PostgreSQL)
- `whatsapp-review-backend` (FastAPI)
- `whatsapp-review-frontend` (React + Nginx)

### Step 3: Access Your Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Database:** localhost:5432

### Step 4: Stop Services

Press `Ctrl+C` in terminal, or:
```bash
docker-compose down
```

---

## Environment Variables

### Create `.env` File

Create `backend/.env` from `backend/.env.example`:

```env
# Postgres DB URL (for Docker Compose, use 'db' as hostname)
DATABASE_URL=postgresql://postgres:postgres@db:5432/reviewsdb

# Twilio Settings - ADD YOUR CREDENTIALS HERE
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=whatsapp:+14155238886

# App settings
APP_HOST=0.0.0.0
APP_PORT=8000
STATE_TTL_SECONDS=1800
```

### Get Your Twilio Credentials

1. Go to: https://console.twilio.com/
2. Find **Account SID** (starts with `AC...`)
3. Find **Auth Token** (click "Show" to reveal)
4. Get **Sandbox Number** from WhatsApp Sandbox page

**Important:** Format phone number as `whatsapp:+14155238886` (include `whatsapp:` prefix)

---

## Twilio WhatsApp Setup

### Step 1: Join WhatsApp Sandbox

1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. You'll see a message: "Join <code> to start"
3. **Send to WhatsApp:** `join <code>` (send to the number shown, usually `+14155238886`)
4. Wait for confirmation message

### Step 2: Install ngrok

**Option A: Download**
- Go to: https://ngrok.com/download
- Download for Windows
- Extract `ngrok.exe` to a folder

**Option B: Using npm**
```bash
npm install -g ngrok
```

**Option C: Using Chocolatey**
```bash
choco install ngrok
```

### Step 3: Configure ngrok

1. **Sign up for free account:** https://dashboard.ngrok.com/signup
2. **Get authtoken:** https://dashboard.ngrok.com/get-started/your-authtoken
3. **Configure:**
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

### Step 4: Start ngrok Tunnel

**Make sure your backend is running first!**

```bash
ngrok http 8000
```

**You'll see:**
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

**⚠️ Keep this terminal open!** If you close it, the URL changes.

### Step 5: Set Webhook in Twilio

1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Scroll to **"WHEN A MESSAGE COMES IN"** section
3. Enter your webhook URL:
   ```
   https://YOUR-NGROK-URL.ngrok.io/whatsapp
   ```
   Example: `https://abc123.ngrok.io/whatsapp`
4. Click **"Save"**

### Step 6: Test It!

1. **Open WhatsApp** on your phone
2. **Send message to:** Your Twilio sandbox number (`+14155238886`)
3. **Send:** `Hi`
4. **Expected flow:**
   - Bot: "Which product is this review for?"
   - You: `iPhone 15`
   - Bot: "What's your name?"
   - You: `John Doe`
   - Bot: "Please send your review for iPhone 15."
   - You: `Great phone, love the camera!`
   - Bot: "Thanks John Doe — your review for iPhone 15 has been recorded."
5. **Check:** http://localhost:3000 - Your review should appear!

---

## Testing

### Test Backend Health

```bash
curl http://localhost:8000/health
```

Should return: `{"status":"ok"}`

### Test Webhook Locally (Without WhatsApp)

```bash
# Start conversation
curl -X POST http://localhost:8000/whatsapp \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hi"

# Provide product name
curl -X POST http://localhost:8000/whatsapp \
  -d "From=whatsapp:+1234567890" \
  -d "Body=iPhone 15"

# Provide name
curl -X POST http://localhost:8000/whatsapp \
  -d "From=whatsapp:+1234567890" \
  -d "Body=John Doe"

# Provide review
curl -X POST http://localhost:8000/whatsapp \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Great phone!"

# Check reviews
curl http://localhost:8000/api/reviews
```

### Test Through ngrok

```bash
curl -X POST https://YOUR-NGROK-URL.ngrok.io/whatsapp \
  -d "From=whatsapp:+1234567890" \
  -d "Body=Hi"
```

### View ngrok Requests

Open in browser: http://localhost:4040

### Backend Tests

```bash
cd backend
pytest -q
```

---

## Project Structure

```
whatsapp-review-collector/
├── backend/              # FastAPI backend
│   ├── app.py           # Main FastAPI application
│   ├── database.py       # SQLAlchemy setup
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── state.py         # Conversation state machine
│   ├── utils.py         # Helper functions
│   ├── requirements.txt # Python dependencies
│   ├── Dockerfile       # Backend Docker image
│   └── tests/          # Unit tests
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.jsx     # Main component
│   │   ├── components/ # React components
│   │   └── styles/     # CSS styles
│   ├── Dockerfile      # Frontend Docker image
│   ├── nginx.conf      # Nginx configuration
│   └── package.json   # Node dependencies
├── docker-compose.yml  # Docker Compose configuration
└── README.md
```

---

## API Endpoints

- **`POST /whatsapp`** - Twilio webhook endpoint (receives WhatsApp messages)
  - Form fields: `From`, `Body`
  - Returns: Plain text response

- **`GET /api/reviews`** - Returns all reviews as JSON
  - Query params: `?limit=100&offset=0`
  - Returns: Array of review objects

- **`GET /health`** - Health check endpoint
  - Returns: `{"status":"ok"}`

---

## Database

**PostgreSQL** is used as the database.

### Connection Details (Docker)
- **Host:** `db` (Docker service name)
- **Port:** `5432`
- **Database:** `reviewsdb`
- **Username:** `postgres`
- **Password:** `postgres`

### Reviews Table Schema

```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    contact_number TEXT NOT NULL,
    user_name TEXT NOT NULL,
    product_name TEXT NOT NULL,
    product_review TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
```

### Access Database

```bash
# Connect to database
docker exec -it whatsapp-review-db psql -U postgres -d reviewsdb

# View all reviews
SELECT * FROM reviews;

# Exit
\q
```

### Backup Database

```bash
docker exec whatsapp-review-db pg_dump -U postgres reviewsdb > backup.sql
```

---

## Troubleshooting

### Services Not Starting

**Problem:** `docker-compose up` fails

**Solutions:**
- Check Docker Desktop is running
- Check ports 3000, 8000, 5432 are free
- Try: `docker-compose up --build --force-recreate`
- Check logs: `docker-compose logs`

### Database Connection Issues

**Problem:** Backend can't connect to database

**Solutions:**
- Wait 10-20 seconds for database to start
- Check database is running: `docker ps`
- Check database logs: `docker-compose logs db`
- Verify DATABASE_URL in `backend/.env`

### ngrok Issues

**Problem:** ngrok URL not working

**Solutions:**
- Make sure backend is running first
- Check: `curl http://localhost:8000/health`
- Verify ngrok is showing "Forwarding" message
- Use HTTPS URL (not HTTP)
- If URL changed, update webhook in Twilio Console

### Webhook Not Receiving Messages

**Problem:** WhatsApp messages not triggering responses

**Solutions:**
1. **Check ngrok is running:**
   ```bash
   curl http://localhost:4040/api/tunnels
   ```

2. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Check webhook URL in Twilio:**
   - Must be HTTPS (not HTTP)
   - Must end with `/whatsapp`
   - Must be accessible (ngrok running)

4. **Check Twilio logs:**
   - Go to: https://console.twilio.com/us1/monitor/logs/errors
   - Look for webhook delivery failures

5. **Check backend logs:**
   ```bash
   docker-compose logs backend
   ```

### Frontend Not Showing Reviews

**Problem:** Reviews not appearing in UI

**Solutions:**
- Check backend API: `curl http://localhost:8000/api/reviews`
- Check database: `docker exec -it whatsapp-review-db psql -U postgres -d reviewsdb -c "SELECT * FROM reviews;"`
- Refresh frontend: http://localhost:3000
- Check browser console for errors

### Port Already in Use

**Problem:** Port 3000, 8000, or 5432 already in use

**Solutions:**
- Stop other services using these ports
- Or change ports in `docker-compose.yml`

---

## Known Limitations

1. **Conversation State:** Stored in memory (`state.py`). If process restarts, ongoing conversations are lost. For production, use Redis or DB-backed `in_progress_reviews` table.

2. **ngrok URLs:** Ephemeral and change when you restart ngrok. Use paid plan for static URLs or deploy to a server.

3. **Twilio Sandbox:** Has usage constraints (shared number, requires joining sandbox). For production, upgrade to dedicated WhatsApp number.

4. **CORS:** Permissive (`allow_origins=["*"]`) for local dev. Lock this down in production.

5. **Security:** Twilio signature validation not implemented. Add for production use.

---

## Common Commands

```bash
# Start all services
docker-compose up --build

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Restart a service
docker-compose restart backend

# Rebuild after code changes
docker-compose up --build

# Check running containers
docker ps

# Connect to database
docker exec -it whatsapp-review-db psql -U postgres -d reviewsdb
```

---

## Quick Reference

### Webhook URL Format
```
https://YOUR-NGROK-URL.ngrok.io/whatsapp
```

### Twilio Console Links
- **Dashboard:** https://console.twilio.com/
- **WhatsApp Sandbox:** https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
- **Logs:** https://console.twilio.com/us1/monitor/logs/errors

### Application URLs
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **ngrok Dashboard:** http://localhost:4040

---

## Next Steps

1. **Test the full flow** with multiple reviews
2. **Monitor Twilio logs** for any issues
3. **Consider upgrading** to a dedicated WhatsApp number (paid)
4. **Add authentication** for production
5. **Implement Redis** for conversation state persistence
6. **Add Twilio signature validation** for security

---

## Support

- **Twilio Docs:** https://www.twilio.com/docs/whatsapp
- **ngrok Docs:** https://ngrok.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/

---

## License

This project is for educational/demonstration purposes.

---

**🎉 You're all set! Happy coding! 🚀**

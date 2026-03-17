# Portfolio Backend (FastAPI)

A production-ready backend for a freelance developer portfolio. Handles contact form submissions, page analytics, and provides an admin dashboard.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+
- MongoDB Atlas Account (Free tier works great)
- SMTP Credentials (Gmail App Password or SendGrid)

### 2. Installation
```bash
cd portfolio-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration
Copy `.env.example` to `.env` and fill in your secrets:
```bash
cp .env.example .env
```

### 4. Run Locally
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. Check `/health` or `/docs` for API documentation.

## 📁 Project Structure
- `main.py`: App entry point & health check.
- `routes/`: API endpoints (Contact, Analytics, Admin).
- `models/`: Pydantic data schemas.
- `services/`: MongoDB and Email logic.
- `middleware/`: CORS and security.

## 🌐 Deployment (Railway)
1. Fork/Push this code to a private GitHub repo.
2. Connect the repo to Railway.app.
3. Add all variables from `.env` to the Railway project settings.
4. Railway will auto-detect the FastAPI app and deploy it.

## 🔒 Security
- **Rate Limiting**: Contact form is limited to 3 submissions per hour per IP.
- **API Key**: Admin routes require `X-API-Key` header.
- **CORS**: Restricted to origins defined in `.env`.

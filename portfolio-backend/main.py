import os
import time
from fastapi import FastAPI, Request
from routes import contact, analytics, admin, bookings
from services.database import connect_to_mongo, close_mongo_connection, db
from middleware.cors import setup_cors
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Nikhil V Portfolio Backend",
    description="Backend for handling contact forms, analytics, and admin dashboard",
    version="1.0.0"
)

# Rate Limiting
app.state.limiter = contact.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
setup_cors(app)

# Events
import socket

async def check_network_connectivity():
    targets = [
        ("smtp.gmail.com", 465),
        ("smtp.gmail.com", 587),
        ("8.8.8.8", 53)  # Google DNS to check general outbound
    ]
    print("DEBUG: Starting network connectivity diagnostics...")
    for host, port in targets:
        try:
            with socket.create_connection((host, port), timeout=5):
                print(f"SUCCESS: Port {port} is OPEN on {host}")
        except Exception as e:
            print(f"FAILURE: Port {port} is CLOSED or TIMED OUT on {host}. Error: {e}")

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    await check_network_connectivity()
    
    # Check for required environment variables
    required_vars = ["EMAIL_HOST", "EMAIL_USER", "EMAIL_PASS", "NOTIFY_EMAIL"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        print(f"CRITICAL WARNING: Missing environment variables: {', '.join(missing)}")
    else:
        print("DEBUG: All email environment variables are present")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Routes
app.include_router(contact.router)
app.include_router(analytics.router)
app.include_router(admin.router)
app.include_router(bookings.router)

@app.get("/health")
async def health_check():
    try:
        # Check DB connection
        await db.client.admin.command('ping')
        db_status = "connected"
    except Exception:
        db_status = "error"
        
    return {
        "status": "ok",
        "db": db_status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/")
async def root():
    return {"message": "Nikhil V Portfolio API is Running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

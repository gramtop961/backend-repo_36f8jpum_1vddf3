from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional
from schemas import LoginRequest, LoginResponse, KYCRequest, KYCStatus, Card, Transaction, DemoEvent
from database import db, create_document, get_documents

app = FastAPI(title="KardX Demo Backend", version="0.1.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

KARDX_API_BASE = os.getenv("KARDX_API_BASE", "https://api.kardx.example.com")

# Health and test endpoints
@app.get("/")
async def root():
    return {"status": "ok", "service": "kardx-demo-backend"}

@app.get("/test")
async def test_db():
    try:
        # Attempt a simple list on a temporary collection
        _ = get_documents("test", {}, limit=1)
        return {"database": "connected"}
    except Exception as e:
        return {"database": "error", "detail": str(e)}

# Auth proxy (demo)
@app.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest):
    # In a real integration, proxy to KardX auth. For demo, generate token
    if not payload.username or not payload.password:
        raise HTTPException(status_code=400, detail="Missing credentials")
    token = f"demo_{payload.username}_token"
    _ = create_document("auth", {"username": payload.username, "token": token})
    return LoginResponse(token=token, expires_in=3600)

@app.post("/kyc", response_model=KYCStatus)
async def kyc_status(req: KYCRequest):
    # Simulate KYC verification lookup
    status = "verified" if req.token.startswith("demo_") else "pending"
    verified = status == "verified"
    _ = create_document("kyc", {"token": req.token, "status": status, "verified": verified})
    return KYCStatus(status=status, verified=verified)

@app.get("/cards", response_model=list[Card])
async def list_cards(token: Optional[str] = None):
    # Demo cards
    data = [
        {"id": "card_1", "last4": "4242", "brand": "Visa", "holder": "KardX User", "exp_month": 12, "exp_year": 2027},
        {"id": "card_2", "last4": "1111", "brand": "Mastercard", "holder": "KardX User", "exp_month": 6, "exp_year": 2026},
    ]
    return [Card(**c) for c in data]

@app.get("/transactions", response_model=list[Transaction])
async def list_transactions(token: Optional[str] = None):
    import datetime
    tx = [
        {"id": "tx_1", "amount": 1299.0, "currency": "INR", "description": "Bill Pay", "status": "success", "created_at": datetime.datetime.utcnow()},
        {"id": "tx_2", "amount": 499.0, "currency": "INR", "description": "Card to Bank Payout", "status": "pending", "created_at": datetime.datetime.utcnow()},
    ]
    return [Transaction(**t) for t in tx]

@app.post("/demo-event")
async def demo_event(event: DemoEvent):
    _ = create_document("demo_events", event)
    return {"ok": True}


from fastapi import FastAPI
from pydantic import BaseModel
from careguard.core import verify

app = FastAPI(
    title="CareGuard AI",
    description="Healthcare AI call-summary verification API",
    version="0.2.0"
)


class VerificationRequest(BaseModel):
    transcript: str
    summary: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/verify")
def verify_summary(request: VerificationRequest):
    result = verify(request.transcript, request.summary)
    return result


@app.get("/")
def home():
    return {
        "message": "Welcome to CareGuard AI",
        "status": "running",
        "documentation": "/docs"
    }

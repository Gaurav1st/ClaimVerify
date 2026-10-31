from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.services import verify_claim

app = FastAPI(title="ClaimVerify API", version="1.0.0",
              description="Evidence retrieval and claim review assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

class ClaimRequest(BaseModel):
    claim: str = Field(min_length=8, max_length=1000)

class Evidence(BaseModel):
    title: str
    url: str
    snippet: str
    source: str

class VerificationResponse(BaseModel):
    claim: str
    verdict: str
    confidence: str
    explanation: str
    evidence: List[Evidence]
    limitations: List[str]

@app.get("/health")
def health():
    return {"status": "ok", "service": "ClaimVerify API"}

@app.post("/verify", response_model=VerificationResponse)
def verify(request: ClaimRequest):
    try:
        return verify_claim(request.claim)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Verification service error: {exc}")

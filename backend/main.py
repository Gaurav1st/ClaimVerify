from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.services import verify_claim
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ClaimVerify API", version="1.0.0",
              description="Evidence retrieval and claim review assistant")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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
    try:
        import os
        groq_configured = bool(os.getenv("GROQ_API_KEY"))
        return {
            "status": "ok",
            "service": "ClaimVerify API",
            "groq_configured": groq_configured
        }
    except Exception as exc:
        logger.error(f"Health check error: {exc}")
        return {"status": "degraded", "service": "ClaimVerify API", "error": str(exc)}

@app.post("/verify", response_model=VerificationResponse)
def verify(request: ClaimRequest):
    try:
        return verify_claim(request.claim)
    except ValueError as exc:
        logger.error(f"Configuration error: {exc}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(exc)}")
    except ConnectionError as exc:
        logger.error(f"Connection error: {exc}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable due to connection issues")
    except TimeoutError as exc:
        logger.error(f"Timeout error: {exc}")
        raise HTTPException(status_code=504, detail="Request timed out. Please try again with a simpler claim")
    except Exception as exc:
        logger.error(f"Unexpected error: {type(exc).__name__}: {exc}")
        raise HTTPException(status_code=502, detail=f"Verification service error: {str(exc)}")

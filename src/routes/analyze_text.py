from fastapi import APIRouter
from src.app.inference import predict_sentiment

router = APIRouter()

@router.post("/analyze-text")
def analyze_text(payload: dict):
    text = payload.get("text", "").strip()

    if not text:
        return {"error": "Empty text"}

    probs, decision = predict_sentiment(text)

    return {
        "probs": probs,
        "decision": decision
    }

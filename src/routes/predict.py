from fastapi import APIRouter
from ..app.schemas import SentimentRequest, SentimentResponse
from ..app.inference import predict_sentiment

router = APIRouter()


@router.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest):
    """
    Analyze a single text and return sentiment probabilities
    and final decision.
    """
    probs, decision = predict_sentiment(request.text)

    return {
        "probabilities": probs,
        "final_decision": decision
    }

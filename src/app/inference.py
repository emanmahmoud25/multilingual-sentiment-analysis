import torch
import torch.nn.functional as F

from .model_loader import model, tokenizer
from src.helper.config import settings


def predict_sentiment(text: str):
    """
    This function takes a text input and predicts its sentiment.

    It returns:
    1) A dictionary with the probability of each sentiment class
    2) The final predicted sentiment label
    """

    # ----------------------------------
    # Step 1: Tokenize the input text
    # ----------------------------------
    # Convert raw text into:
    # - input_ids: numbers that represent words/subwords
    # - attention_mask: indicates real tokens vs padding
    inputs = tokenizer(
        text,
        return_tensors="pt",   # Return PyTorch tensors
        truncation=True,       # Cut text if it is too long
        padding=True           # Pad text to required length
    )

    # ----------------------------------
    # Step 2: Model inference
    # ----------------------------------
    # Disable gradient calculation (faster and less memory)
    with torch.no_grad():
        outputs = model(**inputs)

    # ----------------------------------
    # Step 3: Convert logits to probabilities
    # ----------------------------------
    # Softmax converts raw scores into probabilities
    # dim=1 means across sentiment classes
    probs = F.softmax(outputs.logits, dim=1)[0]

    # ----------------------------------
    # Step 4: Create probabilities dictionary
    # ----------------------------------
    probabilities = {
        # ID2LABEL[i] -> sentiment name (Negative / Neutral / Positive)
        # probs[i]    -> probability of this sentiment
        # * 100       -> convert to percentage
        # round(...,2)-> keep 2 decimal places
        settings.ID2LABEL[i]: round(float(probs[i]) * 100, 2)
        for i in range(len(probs))
    }

    # ----------------------------------
    # Step 5: Final decision
    # ----------------------------------
    # Select the sentiment with the highest probability
    final_decision = max(probabilities, key=probabilities.get)

    return probabilities, final_decision

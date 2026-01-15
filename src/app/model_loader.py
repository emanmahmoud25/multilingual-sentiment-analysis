from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.helper.config import settings


tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_PATH , fix_mistral_regex=True)
model = AutoModelForSequenceClassification.from_pretrained(settings.MODEL_PATH)

model.eval()

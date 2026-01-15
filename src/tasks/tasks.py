import os
import uuid
import pandas as pd
import logging

from src.celery_app import celery_app
from src.app.inference import predict_sentiment
from src.utils.wordcloud_utils import generate_wordcloud_base64
from src.utils.pie_chart import generate_pie_chart_base64

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="analyze_file_task")
def analyze_file_task(self, texts):
    logger.info(f"🚀 Task started | texts count = {len(texts)}")

    sentiments = []
    confidences = []

    for i, text in enumerate(texts):
        try:
            probs, decision = predict_sentiment(text)
            sentiments.append(decision)
            confidences.append(round(max(probs.values()), 4))
        except Exception as e:
            logger.exception(f"❌ Error in predict_sentiment at index {i}")
            raise e

    df = pd.DataFrame({
        "text": texts,
        "sentiment": sentiments,
        "score": confidences
    })

    logger.info("✅ DataFrame created")

    summary = df["sentiment"].value_counts().to_dict()
    logger.info(f"📊 Summary = {summary}")

    # WORDCLOUD
    try:
        wordclouds = {
            "positive": generate_wordcloud_base64(
                df[df.sentiment == "Positive"]["text"]
            ),
            "negative": generate_wordcloud_base64(
                df[df.sentiment == "Negative"]["text"]
            ),
            "neutral": generate_wordcloud_base64(
                df[df.sentiment == "Neutral"]["text"]
            ),
        }
        logger.info("🖼 Wordclouds generated")
    except Exception:
        logger.exception("❌ Wordcloud generation failed")
        raise

    # PIE
    pie_chart = generate_pie_chart_base64(summary)
    logger.info("🥧 Pie chart generated")

    # SAVE FILE
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    OUTPUT_DIR = os.path.join(ROOT_DIR, "Data_Predictions")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_id = str(uuid.uuid4())
    filename = f"sentiment_result_{file_id}.csv"
    output_path = os.path.join(OUTPUT_DIR, filename)

    df.to_csv(output_path, index=False)
    logger.info(f"💾 File saved at {output_path}")

    result = {
        "summary": summary,
        "total_reviews": len(df),
        "wordclouds": wordclouds,
        "pie_chart": pie_chart,
        "data": df.to_dict(orient="records"),
        "filename": filename
    }

    logger.info("🎉 Task finished successfully")
    return result

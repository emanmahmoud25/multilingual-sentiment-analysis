from pydantic_settings import BaseSettings
from typing import Dict
import json


class Settings(BaseSettings):
    # =========================
    # App
    # =========================
    APP_NAME: str = "Sentiment Analysis"
    APP_DESCRIPTION: str = "Sentiment analysis for Arabic and English text"
    APP_ENV: str = "development"
    DEBUG: bool = False

    # =========================
    # Model
    # =========================
    MODEL_PATH: str
    ID2LABEL: Dict[int, str]

    # =========================
    # WordCloud
    # =========================
    WORDCLOUD_WIDTH: int = 900
    WORDCLOUD_HEIGHT: int = 450
    WORDCLOUD_MAX_WORDS: int = 200
    WORDCLOUD_COLORMAP: str = "plasma"
    WORDCLOUD_FONT_PATH: str

    # =========================
    # Celery
    # =========================
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TASK_ALWAYS_EAGER: bool = False

    # =========================
    # Redis
    # =========================
    REDIS_HOST: str
    REDIS_PORT: int

    # =========================
    # Export
    # =========================
    EXPORT_FORMAT: str = "csv"
    EXPORT_ENCODING: str = "utf-8"

    class Config:
        env_file = ".env"

    @classmethod
    def model_validate(cls, values):
        if isinstance(values.get("ID2LABEL"), str):
            values["ID2LABEL"] = {
                int(k): v for k, v in json.loads(values["ID2LABEL"]).items()
            }
        return super().model_validate(values)


settings = Settings()

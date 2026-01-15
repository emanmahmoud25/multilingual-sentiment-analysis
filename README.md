# Multilingual Sentiment Analysis (Arabic & English)

A **production-ready multilingual sentiment analysis system** built using **XLM-RoBERTa**, supporting **Arabic and English** text.

---

## Overview

This project performs **sentiment analysis** on Arabic and English text and classifies each input into:

* Negative
* Neutral
* Positive

The system covers the full pipeline:
**data preprocessing, model training, evaluation, and deployment using FastAPI, Celery, Redis, and Docker**.

---

## Model Performance

Final evaluation on the test set:

| Metric               | Score |
| -------------------- | ----- |
| Accuracy             | ~0.80 |
| Precision (weighted) | 0.79  |
| Recall (weighted)    | 0.79  |
| F1-score (weighted)  | 0.79  |

Class-wise performance:

| Class    | Precision | Recall | F1   |
| -------- | --------- | ------ | ---- |
| Negative | 0.82      | 0.79   | 0.80 |
| Neutral  | 0.64      | 0.65   | 0.64 |
| Positive | 0.87      | 0.88   | 0.88 |

The Neutral class shows slightly lower performance, which is expected in sentiment analysis tasks due to overlapping semantics.

---

## Datasets and Training Strategy

### Arabic Dataset

* **Arabic 100K Reviews**
* Source:
  [https://www.kaggle.com/datasets/abedkhooli/arabic-100k-reviews/data](https://www.kaggle.com/datasets/abedkhooli/arabic-100k-reviews/data)
* Original size: **100,000 reviews**

---

## Back Translation (Data Augmentation)

To improve robustness and increase Arabic data diversity, **Back Translation** was applied.

### What is Back Translation?

A sentence is:

1. Translated from **Arabic → English**
2. Translated back from **English → Arabic**

The meaning is preserved while wording changes slightly, helping the model focus on **semantic meaning instead of memorizing phrases**.

---

### Why Back Translation?

* Increase Arabic training data
* Reduce overfitting
* Improve generalization
* Generate natural paraphrases
* Reduce bias toward English data

---

### Back Translation Strategy

* Original Arabic samples: **100,000**
* Sentences with **≤ 15 words**: **30,000**
* Randomly selected **50%** for augmentation → **15,000**
* Each sentence generated **one additional paraphrase**

Final Arabic dataset size:

```
100,000 original
+15,000 augmented
------------------
115,000 total
```

---

### Back Translation Example

Original:

```
الخدمة كانت ممتازة جدًا
```

Arabic → English:

```
The service was very excellent
```

English → Arabic:

```
كانت الخدمة رائعة للغاية
```

---

### English Dataset

* **Amazon Fine Food Reviews**
* Source:
  [https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews)
* Original size: ~500,000 reviews

**Processing steps:**

* Converted ratings into sentiment labels
* Selected a **balanced random subset**
* Final size: **150,000 reviews**

This prevents the model from being biased toward English.

---

## Preventing Language Bias

| Language | Samples |
| -------- | ------- |
| Arabic   | 115,000 |
| English  | 150,000 |

Both datasets were merged into **one unified multilingual dataset** before training.

---

## Model Details

* Architecture: **XLM-RoBERTa**
* Task: Multiclass sentiment classification
* Classes: Negative, Neutral, Positive
* Framework: Hugging Face Transformers

---

## Trained Model

Model files:
[https://drive.google.com/drive/folders/1flxWB2PE9O3YYMvHFnDZQpaJ2ljnyP2E](https://drive.google.com/drive/folders/1flxWB2PE9O3YYMvHFnDZQpaJ2ljnyP2E)

Example usage:

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained("MODEL_NAME")
tokenizer = AutoTokenizer.from_pretrained("MODEL_NAME")
```

---

## Project Structure

## Project Structure

```
SENTIMENT_ANALYSIS/
│
├── .conda/                     # Virtual environment
├── Data/                       # Raw datasets (Arabic & English)
├── Data_Predictions/           # Saved prediction outputs
│
├── Docker/                     # Docker configuration
│   ├── Dockerfile
│   └── .dockerignore
│
├── src/                        # Main source code
│   │
│   ├── app/                    # Core application logic
│   │   ├── inference.py        # Model inference logic
│   │   ├── model_loader.py     # Load XLM-RoBERTa model
│   │   └── schemas.py          # Request & response schemas
│   │
│   ├── frontend/               # Frontend interface
│   │   ├── templates/          # HTML pages
│   │   ├── static/             # CSS & JavaScript
│   │   └── summary.py          # Frontend summary logic
│   │
│   ├── helper/                 # Helper functions
│   │   └── config.py           # Configuration & label mapping
│   │
│   ├── model/                  # Trained models
│   │   ├── xlm_sentiment_model
│   │   └── arabic-english-sentiment-model
│   │
│   ├── notebook_files/         # Jupyter notebooks
│   │   ├── Cleaning & Augmentation
│   │   ├── EDA
│   │   └── Training
│   │
│   ├── routes/                 # API endpoints
│   │   ├── analyze_text.py     # Text sentiment analysis
│   │   ├── analyze_file.py     # File sentiment analysis
│   │   ├── predict.py          # Prediction endpoint
│   │   ├── download.py         # Download results
│   │   └── task_result.py      # Async task results
│   │
│   ├── tasks/                  # Background processing
│   │   └── tasks.py            # Celery tasks
│   │
│   ├── utils/                  # Utility functions
│   │   ├── pie_chart.py        # Visualization utilities
│   │   └── wordcloud_utils.py  # Word cloud generation
│   │
│   ├── celery_app.py           # Celery configuration
│   └── main.py                 # FastAPI entry point
│
├── .env                        # Environment variables
├── .env.example                # Example environment file
├── .gitignore                  # Ignored files
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies

---

## How to Run the Project

### Run Without Docker

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Open:

```
http://127.0.0.1:8000
```

---

### Run With Docker (Recommended)

```bash
docker build -t sentiment-api -f Docker/Dockerfile .
docker run -p 8000:8000 sentiment-api
```

#### Run Redis

```bash
docker run -d -p 6381:6379 --name redis-sentiment redis
```

#### Start Celery Worker

```bash
celery -A src.celery_app.celery_app worker --pool=solo --loglevel=info
```

Open:

```
http://localhost:8000
```

The project is **Ready to Run using Docker with no setup complexity**.

---

## API Usage

**Endpoint**

```
POST /predict
```

**Request**

```json
{
  "text": "الخدمة ممتازة جدًا"
}
```

**Response**

```json
{
  "probabilities": {
    "Negative": 2.3,
    "Neutral": 5.1,
    "Positive": 92.6
  },
  "final_decision": "Positive"
}
```

---

## Example Predictions

| Text                     | Prediction |
| ------------------------ | ---------- |
| أنا مبسوطة جدًا بالمنتج  | Positive   |
| This product is terrible | Negative   |
| اليوم كان عادي           | Neutral    |

---

## Ignored Files

The `.gitignore` file excludes:

* Data
* Models
* Checkpoints
* Logs
* Notebook checkpoints


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

```
SENTIMENT_ANALYSIS/
│
├── .conda/
├── Data/
├── Data_Predictions/
│
├── Docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .dockerignore
│   ├── .env
│   └── .env.example
│
├── src/
│   ├── app/
│   │   ├── inference.py
│   │   ├── model_loader.py
│   │   └── schemas.py
│   │
│   ├── frontend/
│   │   ├── templates/
│   │   ├── static/
│   │   └── summary.py
│   │
│   ├── helper/
│   │   └── config.py
│   │
│   ├── model/
│   │   ├── xlm_sentiment_model
│   │   └── arabic-english-sentiment-model
│   │
│   ├── notebook_files/
│   │   ├── Cleaning & Augmentation
│   │   ├── EDA
│   │   └── Training
│   │
│   ├── routes/
│   │   ├── analyze_text.py
│   │   ├── analyze_file.py
│   │   ├── predict.py
│   │   ├── download.py
│   │   └── task_result.py
│   │
│   ├── tasks/
│   │   └── tasks.py
│   │
│   ├── utils/
│   │   ├── pie_chart.py
│   │   └── wordcloud_utils.py
│   │
│   ├── celery_app.py
│   └── main.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## How to Run the Project

### Prerequisites

Make sure you have the following installed:

* Docker
* Docker Compose

> No need to install Python, Redis, or Celery locally.

---

## Download the Model (Required)

This project does **not** include the trained model files in the repository due to size limitations.

### Steps

1. Download the model from Google Drive:

```
https://drive.google.com/drive/folders/1flxWB2PE9O3YYMvHFnDZQpaJ2ljnyP2E
```

2. Extract the downloaded folder.

3. Place it at:

```
src/model/xlm_sentiment_model
```

4. Update `.env`:

```env
MODEL_PATH=src/model/xlm_sentiment_model
```

### Important Notes

* The application **will not start** without the model files.
* Do not rename the folder unless you update `MODEL_PATH`.
* The same model path is used by **FastAPI and Celery**.

---

## Run With Docker (Recommended)

### Step 1: Clone the repository

```bash
git clone https://github.com/emanmahmoud25/multilingual-sentiment-analysis.git
cd multilingual-sentiment-analysis/Docker
```

---

### Step 2: Build and run

```bash
docker-compose up --build
```

---

### Step 3: Open the application

```
http://localhost:8000
```

Swagger docs:

```
http://localhost:8000/docs
```

---

### Step 4: Stop services

```bash
docker-compose down
```

---

## Run Without Docker (Optional)

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Requirements:

* Python 3.10
* Redis running
* Celery worker running

---

## API Endpoints Overview

* **Text prediction** → synchronous
* **File analysis** → asynchronous (Celery)

---

## 1️⃣ Predict Sentiment (Text – Sync)

```
POST /predict
```

---

## 2️⃣ Analyze File (Async – Celery)

```
POST /analyze-file
```

---

## 3️⃣ Get Task Result

```
GET /api/task-result/{task_id}
```

---

## 4️⃣ Download Result File

```
GET /api/download?path=results/sentiment_results.csv
```

---

## Ignored Files

The `.gitignore` file excludes:

* Data
* Models
* Checkpoints
* Logs
* Notebook checkpoints
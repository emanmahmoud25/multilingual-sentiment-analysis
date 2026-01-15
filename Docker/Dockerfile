FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

# Install CPU-only PyTorch (compatible with Python 3.10)
RUN pip install torch==2.2.2 \
    --index-url https://download.pytorch.org/whl/cpu

# Install the rest
RUN pip install -r requirements.txt

COPY src ./src

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

from fastapi import APIRouter, UploadFile, File
import pandas as pd
from src.tasks.tasks import analyze_file_task

router = APIRouter()


@router.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        return {"error": "Unsupported file type"}

    df = (
        pd.read_csv(file.file)
        if file.filename.endswith(".csv")
        else pd.read_excel(file.file)
    )

    if "text" not in df.columns:
        return {"error": "File must contain 'text' column"}

    # Send task to Celery
    task = analyze_file_task.delay(df["text"].astype(str).tolist())

    return {
        "message": "File is being processed",
        "task_id": task.id
    }

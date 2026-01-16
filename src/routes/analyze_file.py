from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from src.tasks.tasks import analyze_file_task

router = APIRouter()

@router.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    contents = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(contents))
    else:
        df = pd.read_excel(BytesIO(contents))

    if "text" not in df.columns:
        raise HTTPException(
            status_code=400,
            detail="File must contain a 'text' column"
        )

    # Send task to Celery
    task = analyze_file_task.delay(df["text"].astype(str).tolist())

    return {
        "message": "File is being processed",
        "task_id": task.id
    }

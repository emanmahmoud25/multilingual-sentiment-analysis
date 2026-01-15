from fastapi import APIRouter
from celery.result import AsyncResult
from src.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/task-result/{task_id}")
def get_task_result(task_id: str):
    logger.info(f"🔍 Checking task {task_id}")

    task = AsyncResult(task_id, app=celery_app)

    logger.info(f"📌 Task state = {task.state}")

    if task.state == "PENDING":
        return {"status": "PENDING"}

    if task.state == "FAILURE":
        logger.error(f"❌ Task failed: {task.info}")
        return {
            "status": "FAILURE",
            "error": str(task.info)
        }

    logger.info("✅ Task SUCCESS – returning result")
    return {
        "status": "SUCCESS",
        "result": task.result
    }

from fastapi import APIRouter

from src.routes.predict import router as predict_router
from src.routes.analyze_file import router as analyze_file_router
from src.routes.task_result import router as task_result_router
from src.routes.download import router as download_router

router = APIRouter()

router.include_router(predict_router, tags=["Predict"])
router.include_router(analyze_file_router, tags=["File Analysis"])
router.include_router(task_result_router, tags=["Task Result"])
router.include_router(download_router, tags=["Download"])

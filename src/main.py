from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.routes import router as api_router
from src.routes.analyze_text import router as analyze_text_router

from src.helper.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
    version="1.0.0"
)



# ================= API ROUTES =================
app.include_router(api_router, prefix="/api")
app.include_router(analyze_text_router, prefix="/api", tags=["Text Analysis"])


# ================= STATIC FILES =================
app.mount(
    "/static",
    StaticFiles(directory="src/frontend/static"),
    name="static"
)

# ================= TEMPLATES =================
templates = Jinja2Templates(directory="src/frontend/templates")

# ================= UI ROUTE =================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from job_hunter.api.routers.jobs import router as jobs_router
from job_hunter.api.routers.stats import router as stats_router
from job_hunter.api.routers.fetch import router as fetch_router
from job_hunter.config.database import Base, engine
from job_hunter.models.job import Job
from job_hunter.models.raw_job import RawJob
import os

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VERSION_FILE = PROJECT_ROOT / "VERSION"


def get_app_version() -> str:
    try:
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "unknown"

app = FastAPI(
    title="Job Hunter IA",
    description="API para búsqueda y análisis de vacantes tecnológicas",
    version=get_app_version(),
)

app.include_router(jobs_router)
app.include_router(stats_router)
app.include_router(fetch_router)

static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.on_event("startup")
def init_database():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "version": get_app_version()}

@app.get("/")
def root():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    return FileResponse(index_path)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from job_hunter.api.routers.jobs import router as jobs_router
from job_hunter.api.routers.stats import router as stats_router
from job_hunter.api.routers.fetch import router as fetch_router
import os

app = FastAPI(
    title="Job Hunter IA",
    description="API para búsqueda y análisis de vacantes tecnológicas",
    version="0.8.0",
)

app.include_router(jobs_router)
app.include_router(stats_router)
app.include_router(fetch_router)

static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/health")
def health():
    version = open("../VERSION").read().strip()
    return {"status": "ok", "version": version}

@app.get("/")
def root():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    return FileResponse(index_path)
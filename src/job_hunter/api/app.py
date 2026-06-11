from fastapi import FastAPI
from job_hunter.api.routers.jobs import router as jobs_router
from job_hunter.api.routers.stats import router as stats_router

app = FastAPI(
    title="Job Hunter IA",
    description="API para búsqueda y análisis de vacantes tecnológicas",
    version="0.8.0",
)

app.include_router(jobs_router)
app.include_router(stats_router)


@app.get("/health")
def health():
    version = open("../VERSION").read().strip()
    return {"status": "ok", "version": version}
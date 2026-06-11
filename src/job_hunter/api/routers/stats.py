from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from job_hunter.api.dependencies import get_db
from job_hunter.repositories.job_repository import JobRepository

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    repository = JobRepository(db)
    jobs = repository.get_all()

    sources = {}
    categories = {}
    seniorities = {}
    modalities = {}

    for job in jobs:
        sources[job.source] = sources.get(job.source, 0) + 1
        categories[job.category] = categories.get(job.category, 0) + 1
        seniorities[job.seniority] = seniorities.get(job.seniority, 0) + 1
        modalities[job.modality] = modalities.get(job.modality, 0) + 1

    return {
        "total": len(jobs),
        "by_source": dict(sorted(sources.items(), key=lambda x: -x[1])),
        "by_category": dict(sorted(categories.items(), key=lambda x: -x[1])),
        "by_seniority": dict(sorted(seniorities.items(), key=lambda x: -x[1])),
        "by_modality": dict(sorted(modalities.items(), key=lambda x: -x[1])),
    }
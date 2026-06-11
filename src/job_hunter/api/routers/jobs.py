from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from job_hunter.api.dependencies import get_db
from job_hunter.repositories.job_repository import JobRepository

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/")
def list_jobs(
    source: str = Query(None),
    category: str = Query(None),
    seniority: str = Query(None),
    modality: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    repository = JobRepository(db)
    jobs = repository.get_all()

    if source:
        jobs = [j for j in jobs if j.source == source]
    if category:
        jobs = [j for j in jobs if j.category == category]
    if seniority:
        jobs = [j for j in jobs if j.seniority == seniority]
    if modality:
        jobs = [j for j in jobs if j.modality == modality]

    total = len(jobs)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = jobs[start:end]

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "data": [
            {
                "id": j.id,
                "title": j.title,
                "company": j.company,
                "location": j.location,
                "work_mode": j.work_mode,
                "salary": j.salary,
                "seniority": j.seniority,
                "modality": j.modality,
                "category": j.category,
                "source": j.source,
                "url": j.url,
                "published_at": j.published_at,
            }
            for j in paginated
        ],
    }


@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    repository = JobRepository(db)
    job = repository.get_by_id(job_id)

    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job no encontrado")

    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "work_mode": job.work_mode,
        "salary": job.salary,
        "seniority": job.seniority,
        "modality": job.modality,
        "category": job.category,
        "description": job.description,
        "source": job.source,
        "url": job.url,
        "published_at": job.published_at,
        "created_at": job.created_at,
    }
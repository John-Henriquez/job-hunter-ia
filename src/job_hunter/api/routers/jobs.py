from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from job_hunter.api.dependencies import get_db
from job_hunter.models.job import Job
from job_hunter.repositories.job_repository import APPLICATION_STATUSES, JobRepository

router = APIRouter(prefix="/jobs", tags=["jobs"])


def serialize_job(job: Job, include_description: bool = False) -> dict:
    data = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "work_mode": job.work_mode,
        "salary": job.salary,
        "seniority": job.seniority,
        "modality": job.modality,
        "category": job.category,
        "source": job.source,
        "url": job.url,
        "published_at": job.published_at,
        "application_status": job.application_status,
    }

    if include_description:
        data["description"] = job.description
        data["created_at"] = job.created_at

    return data


@router.get("/")
def list_jobs(
    source: str = Query(None),
    category: str = Query(None),
    seniority: str = Query(None),
    modality: str = Query(None),
    work_mode: str = Query(None),
    application_status: str = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    repository = JobRepository(db)
    jobs, total = repository.search(
        source=source,
        category=category,
        seniority=seniority,
        modality=modality,
        work_mode=work_mode,
        application_status=application_status,
        search=search,
        page=page,
        per_page=per_page,
    )

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "data": [serialize_job(j) for j in jobs],
    }


@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    repository = JobRepository(db)
    job = repository.get_by_id(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")

    return serialize_job(job, include_description=True)


@router.patch("/{job_id}/status")
def update_application_status(
    job_id: int,
    status: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    if status not in APPLICATION_STATUSES:
        raise HTTPException(
            status_code=422,
            detail=f"Estado invalido. Valores permitidos: {sorted(APPLICATION_STATUSES)}",
        )

    repository = JobRepository(db)
    job = repository.update_application_status(job_id, status)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")

    return serialize_job(job, include_description=True)

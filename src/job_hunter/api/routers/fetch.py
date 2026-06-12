from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from job_hunter.api.dependencies import get_db
from job_hunter.providers.registry import ProviderRegistry
from job_hunter.providers.getonboard_provider import GetOnBoardProvider
from job_hunter.providers.arbeitnow_provider import ArbeitnowProvider
from job_hunter.repositories.raw_job_repository import RawJobRepository
from job_hunter.repositories.job_repository import JobRepository
from job_hunter.services.fetch_service import FetchService

router = APIRouter(prefix="/fetch", tags=["fetch"])

_fetch_status = {"running": False, "last_result": None}


def build_registry(provider_name: str = None) -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(GetOnBoardProvider())
    registry.register(ArbeitnowProvider())

    if provider_name:
        provider = registry.get_by_name(provider_name)
        if not provider:
            return None
        single = ProviderRegistry()
        single.register(provider)
        return single

    return registry


def run_fetch(provider_name: str = None):
    from job_hunter.config.database import SessionLocal
    _fetch_status["running"] = True
    db = SessionLocal()
    try:
        registry = build_registry(provider_name)
        raw_repository = RawJobRepository(db)
        job_repository = JobRepository(db)
        fetch_service = FetchService(
            registry=registry,
            raw_repository=raw_repository,
            job_repository=job_repository,
        )
        result = fetch_service.run()
        _fetch_status["last_result"] = result
    finally:
        db.close()
        _fetch_status["running"] = False


@router.post("/")
def fetch_all(background_tasks: BackgroundTasks):
    if _fetch_status["running"]:
        raise HTTPException(status_code=409, detail="Fetch ya en progreso")
    background_tasks.add_task(run_fetch)
    return {"status": "iniciado", "provider": "all"}


@router.post("/{provider_name}")
def fetch_provider(provider_name: str, background_tasks: BackgroundTasks):
    if _fetch_status["running"]:
        raise HTTPException(status_code=409, detail="Fetch ya en progreso")
    registry = build_registry(provider_name)
    if not registry:
        raise HTTPException(status_code=404, detail=f"Provider '{provider_name}' no encontrado")
    background_tasks.add_task(run_fetch, provider_name)
    return {"status": "iniciado", "provider": provider_name}


@router.get("/status")
def fetch_status():
    return _fetch_status
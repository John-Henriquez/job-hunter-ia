from job_hunter.config.database import engine, SessionLocal, Base
from job_hunter.models.job import Job
from job_hunter.models.raw_job import RawJob
from job_hunter.repositories.raw_job_repository import RawJobRepository
from job_hunter.services.raw_job_service import RawJobService
from job_hunter.providers.registry import ProviderRegistry
from job_hunter.providers.getonboard_provider import GetOnBoardProvider
from job_hunter.services.fetch_service import FetchService



def main():
    print(" Job Hunter AI iniciado...")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try: 
        registry = ProviderRegistry()
        registry.register(GetOnBoardProvider())

        repository = RawJobRepository(db)
        fetch_service = FetchService(registry, repository)
        fetch_service.run()

    finally:
        db.close()

if __name__ == "__main__":
    main()
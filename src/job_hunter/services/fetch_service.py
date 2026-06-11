from job_hunter.providers.registry import ProviderRegistry
from job_hunter.services.raw_job_service import RawJobService
from job_hunter.repositories.raw_job_repository import RawJobRepository


class FetchService:

    def __init__(self, registry: ProviderRegistry, repository: RawJobRepository):
        self.registry = registry
        self.service = RawJobService(repository)
        self.repository = repository

    def run(self) -> dict:
        total_saved = 0
        total_skipped = 0

        for provider in self.registry.get_all():
            print(f"\n[{provider.source_name}] Iniciando fetch...")

            raw_jobs = provider.fetch_jobs()
            parsed_jobs = provider.parse_jobs(raw_jobs)
            saved = 0

            for job in parsed_jobs:
                existing = self.repository.get_by_external_id(job["external_id"])
                if existing:
                    total_skipped += 1
                    continue

                self.service.save_raw_job(
                    source=job["source"],
                    external_id=job["external_id"],
                    raw_payload=job["raw_payload"],
                )
                saved += 1

            total_saved += saved
            print(f"[{provider.source_name}] Guardados: {saved} | Duplicados: {len(parsed_jobs) - saved}")

        print(f"\nResumen total:")
        print(f"  Guardados : {total_saved}")
        print(f"  Duplicados: {total_skipped}")

        return {
            "saved": total_saved,
            "skipped": total_skipped,
        }
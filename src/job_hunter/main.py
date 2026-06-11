import argparse
from job_hunter.config.database import engine, SessionLocal, Base
from job_hunter.models.job import Job
from job_hunter.models.raw_job import RawJob
from job_hunter.providers.registry import ProviderRegistry
from job_hunter.providers.getonboard_provider import GetOnBoardProvider
from job_hunter.repositories.raw_job_repository import RawJobRepository
from job_hunter.repositories.job_repository import JobRepository
from job_hunter.services.fetch_service import FetchService
from job_hunter.normalizers.getonboard_normalizer import GetOnBoardNormalizer


def build_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(GetOnBoardProvider())
    return registry


def cmd_fetch(args):
    db = SessionLocal()
    try:
        registry = build_registry()

        if args.provider:
            provider = registry.get_by_name(args.provider)
            if not provider:
                print(f"Provider '{args.provider}' no encontrado.")
                print(f"Disponibles: {registry.list_registered()}")
                return
            single = ProviderRegistry()
            single.register(provider)
            registry = single

        raw_repository = RawJobRepository(db)
        job_repository = JobRepository(db)
        normalizer = GetOnBoardNormalizer()

        fetch_service = FetchService(
            registry=registry,
            raw_repository=raw_repository,
            job_repository=job_repository,
            normalizer=normalizer,
        )
        fetch_service.run()
    finally:
        db.close()


def cmd_stats(args):
    db = SessionLocal()
    try:
        from job_hunter.repositories.job_repository import JobRepository
        repository = JobRepository(db)
        jobs = repository.get_all()

        print(f"\nEstadísticas:")
        print(f"  Total jobs: {len(jobs)}")

        sources = {}
        categories = {}
        for job in jobs:
            sources[job.source] = sources.get(job.source, 0) + 1
            categories[job.category] = categories.get(job.category, 0) + 1

        print(f"\n  Por fuente:")
        for source, count in sorted(sources.items(), key=lambda x: -x[1]):
            print(f"    {source}: {count}")

        print(f"\n  Por categoría:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"    {cat}: {count}")
    finally:
        db.close()


def main():
    print("Job Hunter AI iniciado...")
    Base.metadata.create_all(bind=engine)

    parser = argparse.ArgumentParser(prog="job-hunter")
    subparsers = parser.add_subparsers(dest="command")

    fetch_parser = subparsers.add_parser("fetch", help="Descarga vacantes")
    fetch_parser.add_argument(
        "--provider",
        type=str,
        help="Nombre del provider (ej: getonboard, indeed). Sin argumento corre todos.",
        default=None,
    )

    subparsers.add_parser("stats", help="Muestra estadísticas de jobs en BD")

    args = parser.parse_args()

    if args.command == "fetch":
        cmd_fetch(args)
    elif args.command == "stats":
        cmd_stats(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
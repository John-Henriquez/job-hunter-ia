from job_hunter.config.database import engine, SessionLocal, Base
from job_hunter.models.job import Job


def main():
    print("Job Hunter IA iniciado 🚀")

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        job = Job(
            title="Python Developer Junior",
            company="Demo Company",
            location="Chile",
            work_mode="remote",
            salary="$1.200.000",
            description="Vacante de prueba",
            source="manual",
            url="https://example.com/job"
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        print(f"Job insertado con ID: {job.id}")

        jobs = db.query(Job).all()

        print("\nJobs en base de datos:")
        for j in jobs:
            print(f"- {j.id} | {j.title} | {j.company}")


if __name__ == "__main__":
    main()
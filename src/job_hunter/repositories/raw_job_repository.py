from job_hunter.models.raw_job import RawJob


class RawJobRepository:

    def __init__(self, db):
        self.db = db

    def create(self, raw_job):
        self.db.add(raw_job)
        self.db.commit()
        self.db.refresh(raw_job)
        return raw_job

    def get_by_external_id(self, external_id):
        return (
            self.db.query(RawJob)
            .filter(RawJob.external_id == external_id)
            .first()
        )

    def get_unprocessed(self):
        return (
            self.db.query(RawJob)
            .filter(RawJob.processed == False)
            .all()
        )
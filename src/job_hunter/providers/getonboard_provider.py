from job_hunter.providers.base_provider import BaseProvider

class GetOnBoardProvider(BaseProvider):
    def fetch_jobs(self):
        print("Obteniendo vacantes desde GetOnBoard...")
        return []
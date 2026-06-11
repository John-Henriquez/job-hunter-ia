import time
import requests
from job_hunter.providers.base_provider import BaseProvider
from job_hunter.normalizers.base_normalizer import BaseNormalizer


class ArbeitnowProvider(BaseProvider):

    BASE_URL = "https://www.arbeitnow.com/api/job-board-api"
    PER_PAGE = 100
    REQUEST_DELAY = 2

    @property
    def source_name(self) -> str:
        return "arbeitnow"

    @property
    def source_version(self) -> str:
        return "1.0"

    def fetch_jobs(self) -> list:
        all_jobs = []
        page = 1

        print(f"[{self.source_name}] Iniciando descarga...")

        while True:
            try:
                response = requests.get(
                    self.BASE_URL,
                    params={"page": page},
                    timeout=15,
                )
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"[{self.source_name}] Error en página {page}: {e}")
                break

            data = response.json()
            jobs = data.get("data", [])

            if not jobs:
                print(f"[{self.source_name}] Sin más vacantes en página {page}. Fin.")
                break

            print(f"[{self.source_name}] Página {page}: {len(jobs)} vacantes")
            all_jobs.extend(jobs)
            page += 1
            time.sleep(self.REQUEST_DELAY)

        print(f"[{self.source_name}] Total descargadas: {len(all_jobs)}")
        return all_jobs

    def parse_jobs(self, raw_jobs: list) -> list[dict]:
        parsed = []
        for item in raw_jobs:
            external_id = item.get("slug", "")
            if not external_id:
                continue

            parsed.append({
                "source": self.source_name,
                "external_id": external_id,
                "raw_payload": item,
            })

        return parsed
    
    def get_normalizer(self) -> BaseNormalizer:
        from job_hunter.normalizers.arbeitnow_normalizer import ArbeitnowNormalizer
        return ArbeitnowNormalizer()
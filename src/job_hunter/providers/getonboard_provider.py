import requests
from job_hunter.providers.base_provider import BaseProvider


class GetOnBoardProvider(BaseProvider):

    BASE_URL = "https://www.getonbrd.com/api/v0"
    PER_PAGE = 100

    @property
    def source_name(self) -> str:
        return "getonboard"
    
    @property
    def source_version(self) -> str:
        return "1.0"

    def _get_categories(self):
        response = requests.get(
            f"{self.BASE_URL}/categories",
            params={"per_page": 100},
            timeout=15,
        )
        response.raise_for_status()
        return response.json().get("data", [])

    def _get_jobs_for_category(self, category_id):
        all_jobs = []
        page = 1

        while True:
            response = requests.get(
                f"{self.BASE_URL}/categories/{category_id}/jobs",
                params={"page": page, "per_page": self.PER_PAGE},
                timeout=15,
            )
            response.raise_for_status()
            jobs = response.json().get("data", [])

            if not jobs:
                break

            all_jobs.extend(jobs)
            page += 1

        return all_jobs

    def fetch_jobs(self):
        all_jobs = []

        print(f"[{self.source_name}] Obteniendo categorías...")
        categories = self._get_categories()
        print(f"[{self.source_name}] {len(categories)} categorías encontradas")

        for cat in categories:
            cat_id = cat.get("id")
            cat_name = cat.get("attributes", {}).get("name", cat_id)

            try:
                jobs = self._get_jobs_for_category(cat_id)
                print(f"[{self.source_name}] {cat_name}: {len(jobs)} vacantes")
                all_jobs.extend(jobs)
            except requests.RequestException as e:
                print(f"[{self.source_name}] Error en categoría {cat_name}: {e}")

        print(f"[{self.source_name}] Total descargadas: {len(all_jobs)}")
        return all_jobs

    def parse_jobs(self, raw_jobs: list) -> list[dict]:
        parsed = []
        for item in raw_jobs:
            external_id = str(item.get("id", ""))
            if not external_id:
                continue

            parsed.append({
                "source": self.source_name,
                "external_id": external_id,
                "raw_payload": item,
            })
        return parsed
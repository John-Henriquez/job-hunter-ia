from unittest.mock import MagicMock
from job_hunter.services.raw_job_service import RawJobService


def test_save_raw_job_nuevo():
    repository = MagicMock()
    repository.get_by_external_id.return_value = None

    service = RawJobService(repository)
    service.save_raw_job(
        source="getonboard",
        external_id="123",
        raw_payload={"title": "Dev"},
    )

    repository.create.assert_called_once()


def test_save_raw_job_duplicado():
    repository = MagicMock()
    repository.get_by_external_id.return_value = MagicMock()

    service = RawJobService(repository)
    result = service.save_raw_job(
        source="getonboard",
        external_id="123",
        raw_payload={"title": "Dev"},
    )

    repository.create.assert_not_called()
    assert result is not None
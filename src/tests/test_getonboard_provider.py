from job_hunter.providers.getonboard_provider import GetOnBoardProvider


PAYLOAD_FIXTURE = [
    {"id": "abc123", "attributes": {"title": "Backend Dev"}},
    {"id": "xyz789", "attributes": {"title": "Data Engineer"}},
    {"id": "", "attributes": {"title": "Sin ID"}},
]


def test_parse_jobs_retorna_lista():
    provider = GetOnBoardProvider()
    result = provider.parse_jobs(PAYLOAD_FIXTURE)
    assert isinstance(result, list)


def test_parse_jobs_filtra_sin_id():
    provider = GetOnBoardProvider()
    result = provider.parse_jobs(PAYLOAD_FIXTURE)
    assert len(result) == 2


def test_parse_jobs_estructura_correcta():
    provider = GetOnBoardProvider()
    result = provider.parse_jobs(PAYLOAD_FIXTURE)
    for job in result:
        assert "source" in job
        assert "external_id" in job
        assert "raw_payload" in job


def test_parse_jobs_source_correcto():
    provider = GetOnBoardProvider()
    result = provider.parse_jobs(PAYLOAD_FIXTURE)
    assert all(job["source"] == "getonboard" for job in result)
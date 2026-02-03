import pytest
import httpx

from learning_lab.api import app


def get_async_client():
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.anyio
async def test_health():
    async with get_async_client() as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_ready():
    async with get_async_client() as ac:
        r = await ac.get("/ready")
    assert r.status_code == 200
    assert r.json() == {"status": "ready"}


@pytest.mark.anyio
async def test_request_id_header_returned():
    async with get_async_client() as ac:
        r = await ac.get("/health", headers={"x-request-id": "test-id-123"})
    assert r.status_code == 200
    assert r.headers.get("x-request-id") == "test-id-123"


@pytest.mark.anyio
async def test_summarise_rejects_non_csv():
    async with get_async_client() as ac:
        files = {"file": ("notes.txt", b"hello", "text/plain")}
        r = await ac.post("/summarise", files=files)
    assert r.status_code == 400


@pytest.mark.anyio
async def test_summarise_accepts_csv():
    csv_bytes = b"name,age,score\nJesal,39,88\n"
    async with get_async_client() as ac:
        files = {"file": ("sample.csv", csv_bytes, "text/csv")}
        r = await ac.post("/summarise", files=files)
    assert r.status_code == 200
    body = r.json()
    assert body["filename"] == "sample.csv"
    assert "Rows: 1" in body["report"]

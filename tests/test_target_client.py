import asyncio

import pytest
from httpx import Response

respx = pytest.importorskip("respx")
pytest.importorskip("pytest_asyncio")

from src.adapter.target_client import TargetClient, TargetClientConfig


def test_extract_response():
    config = TargetClientConfig(
        base_url="http://example.com",
        endpoint="/api",
        request_key="prompt",
        response_key="response",
        model="test",
    )
    client = TargetClient(config, timeout_seconds=5, max_retries=0, semaphore=asyncio.Semaphore(1))
    assert client.extract_response({"response": "ok"}) == "ok"


@respx.mock
@pytest.mark.asyncio
async def test_target_client_send():
    config = TargetClientConfig(
        base_url="http://example.com",
        endpoint="/api",
        request_key="prompt",
        response_key="response",
        model="test",
    )
    respx.post("http://example.com/api").mock(return_value=Response(200, json={"response": "ok"}))
    client = TargetClient(config, timeout_seconds=5, max_retries=0, semaphore=asyncio.Semaphore(1))
    payload = await client.send("hello")
    assert payload["response"] == "ok"

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

from src.core.logger import env_or_none, mask_secret


@dataclass
class TargetClientConfig:
    base_url: str
    endpoint: str
    request_key: str
    response_key: str
    model: str
    api_key_env: Optional[str] = None


class TargetClient:
    def __init__(self, config: TargetClientConfig, timeout_seconds: int, max_retries: int, semaphore: asyncio.Semaphore) -> None:
        self.config = config
        self.timeout = timeout_seconds
        self.max_retries = max_retries
        self.semaphore = semaphore

    async def send(self, prompt: str) -> Dict[str, Any]:
        url = f"{self.config.base_url}{self.config.endpoint}"
        headers = {}
        api_key = env_or_none(self.config.api_key_env)
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {self.config.request_key: prompt, "model": self.config.model, "stream": False}
        return await self._request(url, payload, headers)

    async def _request(self, url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
        retry = 0
        async with self.semaphore:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                while True:
                    try:
                        response = await client.post(url, json=payload, headers=headers)
                        if response.status_code >= 500 or response.status_code == 429:
                            raise httpx.HTTPStatusError("retryable", request=response.request, response=response)
                        response.raise_for_status()
                        return response.json()
                    except httpx.HTTPStatusError:
                        if retry >= self.max_retries:
                            raise
                        retry += 1
                        await asyncio.sleep(2 ** retry)
                    except httpx.RequestError:
                        if retry >= self.max_retries:
                            raise
                        retry += 1
                        await asyncio.sleep(2 ** retry)

    def extract_response(self, payload: Dict[str, Any]) -> str:
        return str(payload.get(self.config.response_key, ""))

    def masked_api_key(self) -> Optional[str]:
        return mask_secret(env_or_none(self.config.api_key_env))

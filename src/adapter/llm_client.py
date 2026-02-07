from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

from src.core.logger import env_or_none, mask_secret


@dataclass
class LLMClientConfig:
    base_url: str
    model: str
    backend: str
    api_key_env: Optional[str] = None


class LLMClient:
    def __init__(self, config: LLMClientConfig, timeout_seconds: int, max_retries: int, semaphore: asyncio.Semaphore) -> None:
        self.config = config
        self.timeout = timeout_seconds
        self.max_retries = max_retries
        self.semaphore = semaphore

    async def generate(self, prompt: str) -> Dict[str, Any]:
        if self.config.backend != "ollama":
            raise ValueError("Unsupported backend")

        url = f"{self.config.base_url}/api/generate"
        headers = {}
        api_key = env_or_none(self.config.api_key_env)
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {"model": self.config.model, "prompt": prompt, "stream": False}

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
                    except httpx.HTTPStatusError as exc:
                        if retry >= self.max_retries:
                            raise
                        retry += 1
                        await asyncio.sleep(2 ** retry)
                    except httpx.RequestError:
                        if retry >= self.max_retries:
                            raise
                        retry += 1
                        await asyncio.sleep(2 ** retry)

    def masked_api_key(self) -> Optional[str]:
        return mask_secret(env_or_none(self.config.api_key_env))

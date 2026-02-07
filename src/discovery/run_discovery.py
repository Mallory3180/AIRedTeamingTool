from __future__ import annotations

import argparse
import asyncio
import uuid
from typing import List

from src.adapter.llm_client import LLMClient, LLMClientConfig
from src.adapter.target_client import TargetClient, TargetClientConfig
from src.core.config import load_system_config, load_target_config
from src.core.logger import RunLogger
from src.core.types import RunLog


async def run_discovery(config_path: str, target_config_path: str) -> str:
    system_config = load_system_config(config_path)
    target_config = load_target_config(target_config_path)

    run_id = uuid.uuid4().hex
    logger = RunLogger(run_id, system_config.logging["logs_root"])

    semaphore = asyncio.Semaphore(system_config.logging["max_concurrency"])

    orchestrator = LLMClient(
        LLMClientConfig(**system_config.orchestrator_llm),
        timeout_seconds=system_config.logging["timeout_seconds"],
        max_retries=system_config.logging["max_retries"],
        semaphore=semaphore,
    )

    target = TargetClient(
        TargetClientConfig(**target_config.__dict__),
        timeout_seconds=system_config.logging["timeout_seconds"],
        max_retries=system_config.logging["max_retries"],
        semaphore=semaphore,
    )

    prompt = "Summarize the system's behavior for a benign prompt."

    try:
        orchestrator_response = await orchestrator.generate(prompt)
        logger.append(
            RunLog(
                run_id=run_id,
                step="discovery",
                llm_role="orchestrator",
                prompt=prompt,
                response=str(orchestrator_response),
                metadata={"api_key": orchestrator.masked_api_key()},
            )
        )
    except Exception as exc:  # noqa: BLE001
        logger.append(
            RunLog(
                run_id=run_id,
                step="discovery",
                llm_role="orchestrator",
                prompt=prompt,
                success=False,
                error_type=type(exc).__name__,
                exception=str(exc),
            )
        )

    try:
        target_payload = await target.send(prompt)
        target_response = target.extract_response(target_payload)
        logger.append(
            RunLog(
                run_id=run_id,
                step="discovery",
                llm_role="target",
                prompt=prompt,
                response=target_response,
                metadata={"api_key": target.masked_api_key()},
            )
        )
    except Exception as exc:  # noqa: BLE001
        logger.append(
            RunLog(
                run_id=run_id,
                step="discovery",
                llm_role="target",
                prompt=prompt,
                success=False,
                error_type=type(exc).__name__,
                exception=str(exc),
            )
        )

    return run_id


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--target-config", required=True)
    args = parser.parse_args(argv)

    asyncio.run(run_discovery(args.config, args.target_config))


if __name__ == "__main__":
    main()

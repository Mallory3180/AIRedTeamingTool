from __future__ import annotations

import argparse

from src.deepdive.run_deepdive import run_deepdive
from src.discovery.run_discovery import run_discovery
from src.report.build_report import build_report


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    discovery_parser = subparsers.add_parser("discovery")
    discovery_parser.add_argument("--config", required=True)
    discovery_parser.add_argument("--target-config", required=True)

    deepdive_parser = subparsers.add_parser("deepdive")
    deepdive_parser.add_argument("--config", required=True)
    deepdive_parser.add_argument("--target-config", required=True)

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("--config", required=True)
    report_parser.add_argument("--run-id")

    args = parser.parse_args()

    if args.command == "discovery":
        import asyncio

        asyncio.run(run_discovery(args.config, args.target_config))
    elif args.command == "deepdive":
        import asyncio

        asyncio.run(run_deepdive(args.config, args.target_config))
    elif args.command == "report":
        build_report(args.config, args.run_id)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from src.core.config import load_system_config


def build_report(config_path: str, run_id: str | None) -> Path:
    system_config = load_system_config(config_path)
    logs_root = Path(system_config.logging["logs_root"])

    if run_id is None:
        run_dirs = sorted(logs_root.glob("run_*/runs.jsonl"))
        if not run_dirs:
            raise FileNotFoundError("No runs.jsonl found")
        run_path = run_dirs[-1]
    else:
        run_path = logs_root / f"run_{run_id}" / "runs.jsonl"

    report_path = run_path.parent / "report.json"
    entries = []
    with run_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            entries.append(json.loads(line))

    report_payload = {
        "run_id": run_path.parent.name.replace("run_", ""),
        "entries": entries,
        "entry_count": len(entries),
    }

    report_path.write_text(json.dumps(report_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-id")
    args = parser.parse_args(argv)

    build_report(args.config, args.run_id)


if __name__ == "__main__":
    main()

# LLM Red Teaming Orchestrator (Scaffold)

## Quickstart

```bash
cp .env.example .env
# edit config/target_config.yaml and config/system_config.yaml for your environment

docker compose up -d

python -m src.rag.ingest --config config/system_config.yaml
python -m src.discovery.run_discovery --config config/system_config.yaml --target-config config/target_config.yaml
python -m src.deepdive.run_deepdive --config config/system_config.yaml --target-config config/target_config.yaml
python -m src.report.build_report --config config/system_config.yaml
```

## Notes
- All logs are append-only JSONL under `data/logs/run_<id>/runs.jsonl`.
- Target and orchestrator LLMs are configured independently.
- Configuration is split between YAML and `.env` for secrets.
- `data/inputs/sample_seed.txt` is included for mini-mode ingestion when PDFs are not available.

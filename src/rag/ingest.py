from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.core.config import load_system_config


def ingest(config_path: str) -> None:
    system_config = load_system_config(config_path)
    rag_cfg = system_config.rag
    embedding_cfg = system_config.embedding

    inputs_dir = Path("data/inputs")
    pdfs = list(inputs_dir.glob("*.pdf"))
    txts = list(inputs_dir.glob("*.txt"))

    embeddings = OllamaEmbeddings(model=embedding_cfg["model"], base_url=embedding_cfg["base_url"])
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=rag_cfg["chunk_size"],
        chunk_overlap=rag_cfg["chunk_overlap"],
    )

    documents = []
    for pdf_path in pdfs:
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        split_docs = splitter.split_documents(docs)
        for idx, doc in enumerate(split_docs):
            doc.metadata.update(
                {
                    "doc_id": pdf_path.name,
                    "page": doc.metadata.get("page", 0),
                    "chunk_id": f"{pdf_path.stem}-{idx}",
                    "source_type": "pdf",
                    "section": doc.metadata.get("section"),
                    "heading": doc.metadata.get("heading"),
                    "rule_id": doc.metadata.get("rule_id"),
                    "rule_type": doc.metadata.get("rule_type"),
                }
            )
            documents.append(doc)

    for txt_path in txts:
        loader = TextLoader(str(txt_path))
        docs = loader.load()
        split_docs = splitter.split_documents(docs)
        for idx, doc in enumerate(split_docs):
            doc.metadata.update(
                {
                    "doc_id": txt_path.name,
                    "page": 0,
                    "chunk_id": f"{txt_path.stem}-{idx}",
                    "source_type": "text",
                    "section": doc.metadata.get("section"),
                    "heading": doc.metadata.get("heading"),
                    "rule_id": doc.metadata.get("rule_id"),
                    "rule_type": doc.metadata.get("rule_type"),
                }
            )
            documents.append(doc)

    if not documents:
        return

    Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=rag_cfg["persist_path"],
    )


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args(argv)
    ingest(args.config)


if __name__ == "__main__":
    main()

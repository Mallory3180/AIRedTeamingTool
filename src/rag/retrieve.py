from __future__ import annotations

from typing import List

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from src.core.config import load_system_config
from src.core.types import RagChunkMetadata, RagResult


def retrieve(query: str, config_path: str) -> List[RagResult]:
    system_config = load_system_config(config_path)
    rag_cfg = system_config.rag
    embedding_cfg = system_config.embedding

    embeddings = OllamaEmbeddings(model=embedding_cfg["model"], base_url=embedding_cfg["base_url"])
    vectorstore = Chroma(
        persist_directory=rag_cfg["persist_path"],
        embedding_function=embeddings,
    )

    docs = vectorstore.similarity_search(query, k=rag_cfg["k"])
    results: List[RagResult] = []
    for doc in docs:
        metadata = RagChunkMetadata(
            doc_id=doc.metadata.get("doc_id", ""),
            page=int(doc.metadata.get("page", 0)),
            chunk_id=doc.metadata.get("chunk_id", ""),
            source_type=doc.metadata.get("source_type", ""),
            section=doc.metadata.get("section"),
            heading=doc.metadata.get("heading"),
            rule_id=doc.metadata.get("rule_id"),
            rule_type=doc.metadata.get("rule_type"),
        )
        quote = doc.page_content[:200]
        results.append(
            RagResult(
                doc_id=metadata.doc_id,
                page=metadata.page,
                quote=quote,
                metadata=metadata,
            )
        )
    return results

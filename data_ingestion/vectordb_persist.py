from typing import Dict

from langchain.document_loaders.base import BaseLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.documents import BaseDocumentTransformer
from langchain_core.vectorstores import VectorStore

from type_extensions import T

from .ingest import ingestion


def vec_db_persist(
    name: str,
    persist_dir: str,
    source_loader: BaseLoader,
    splitter: BaseDocumentTransformer,
    chunk_size: int,
    chunk_overlap: int,
    vec_store: VectorStore,
    embedding: OpenAIEmbeddings,
    **kwargs: Dict[str, T]
) -> VectorStore:
    vectordb = ingestion(
        name,
        source_loader,
        splitter,
        chunk_size,
        chunk_overlap,
        persist_dir,
        vec_store,
        embedding,
        **kwargs
    )

    # persiste the db to disk
    vectordb.persist()
    vectordb = None

    return vectordb

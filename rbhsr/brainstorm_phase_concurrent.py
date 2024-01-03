import json
import queue
import threading
from typing import Tuple, Union

from langchain.pydantic_v1 import BaseModel
from langchain.schema.embeddings import Embeddings
from langchain.schema.vectorstore import VectorStore

from shared import get_cb
from type_extensions import T
from utils import custom_timer_with_return

from .brainstorm_chain import llm_chain_brainstorm
from .concurrent_brainstorm import brainstorm_with_concurrency
from .rerank import co


@get_cb
@custom_timer_with_return
def brainstorm_concurrent(
    top_n_rerank: int,
    user_query: str,
    notes: str,
    queries: str,
    vec_store: VectorStore,
    persist_dir: str,
    embedding_function: Union[BaseModel, Embeddings],
    **kwargs: dict[str, T],
) -> Tuple[str, str]:
    """Brainstorm using retrieved documents from a source

    Args:
        top_n_rerank (int): Top n reranked documents
        user_query (str): User query
        notes (str): Content for answering the query
        queries (str): Previous queries
        vec_store (VectorStore): The vector store
        persist_directory (str): Directory for data persistence
        embedding (Union[BaseModel, Embeddings]): Embedding for vector storage

    Returns:
        Tuple[str, str]: Tuple of queries and notes
    """

    # Retrieve relevant resources from persisted vector store
    vectordb = vec_store(
        persist_directory=persist_dir, embedding_function=embedding_function
    )
    init_resources = vectordb.similarity_search(user_query)
    init_docs_resources = [
        init_resources[i].page_content for i in range(len(init_resources))
    ]

    # Rerank the relevant documents to the user query
    rerank_docs = co.rerank(
        query=user_query,
        documents=init_docs_resources,
        top_n=top_n_rerank,
        model="rerank-english-v2.0",
    )
    reranked_init_docs_resources = [
        rerank_doc.document["text"] for rerank_doc in rerank_docs
    ]
    chunks = f"{reranked_init_docs_resources}"

    # Create queries for brainstorming
    response = llm_chain_brainstorm(user_query, queries, notes, chunks, **kwargs)

    # Questions to be asked during search in json format
    questions = json.loads(response)
    top_questions = questions["queries"]

    num_threads = len(top_questions)

    queue_brainstorm = {f"bs_{i}": queue.Queue() for i, _ in enumerate(top_questions)}
    queue_result = {f"rs_{i}": queue.Queue() for i, _ in enumerate(top_questions)}

    # Loop through the relevant questions
    for i in range(num_threads):
        question = top_questions[i]
        queue_brainstorm[f"bs_{i}"].put(question)

    # Create threads
    brainstorm_threads = {
        f"bs_{i}": threading.Thread(
            target=brainstorm_with_concurrency,
            args=(
                queue_brainstorm[f"bs_{i}"],
                queue_result[f"rs_{i}"],
                top_n_rerank,
                vectordb,
            ),
        )
        for i, _ in enumerate(top_questions)
    }

    threads_bs = []
    for i, _ in enumerate(top_questions):
        brainstorm_threads[f"bs_{i}"].start()
        threads_bs.append(brainstorm_threads[f"bs_{i}"])

    for thread_bs in threads_bs:
        thread_bs.join()

    for i in range(num_threads):
        top_status = 0
        for question, compressed_content in queue_result[f"rs_{i}"].get().items():
            if top_status == 0:
                top_note = compressed_content
                top_status += 1
            notes = f"{notes}\n\n SOURCE: \n NOTE: {compressed_content}"
            queries = f"{queries}\n QUESTION: {question}"

    return queries, notes, top_note

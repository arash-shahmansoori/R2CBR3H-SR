from queue import Queue
from typing import List

from langchain.schema.vectorstore import VectorStore

from .refine_phase import refine
from .rerank import co


def brainstorm_with_concurrency(
    queue_brainstorm: Queue,
    queue_result: Queue,
    top_n_rerank: int,
    vectordb: VectorStore,
) -> List[str]:
    """Concurrent brainstorming

    Args:
        queue_brainstorm (Queue): The queue containing the brainstorming
        queue_result (Queue): The queue containing the results
        top_n_rerank (int): Top n reranked documents
        vectordb (VectorStore): The vector store
    """

    while not queue_brainstorm.empty():
        # Get the question from the queue
        question = queue_brainstorm.get()

        # Retrieve contents for a givent question from the source
        resources = vectordb.similarity_search(question)
        docs_resources = [resource.page_content for resource in resources]

        # Rerank the relevant documents to the top questions
        rerank_docs_per_query = co.rerank(
            query=question,
            documents=docs_resources,
            top_n=top_n_rerank,
            model="rerank-english-v2.0",
        )
        reranked_docs_per_query_resources = [
            rerank_doc_per_query.document["text"]
            for rerank_doc_per_query in rerank_docs_per_query
        ]

        # Compress the contents of reranked documents
        (compressed_content, _), _ = refine(reranked_docs_per_query_resources)
        queue_result.put({question: compressed_content})

        # Mark the task as done
        queue_brainstorm.task_done()

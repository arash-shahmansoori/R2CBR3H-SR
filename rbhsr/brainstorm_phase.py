import json
from typing import Tuple

from langchain.schema.vectorstore import VectorStore
from tqdm import tqdm

from shared import get_cb
from type_extensions import T
from utils import custom_timer_with_return

from .brainstorm_chain import llm_chain_brainstorm_baseline
from .refine_phase import refine


@get_cb
@custom_timer_with_return
def brainstorm(
    user_query: str,
    notes: str,
    queries: str,
    vec_store: VectorStore,
    persist_dir,
    embedding_function,
    **kwargs: dict[str, T],
) -> Tuple[str, str]:
    """Brainstorm using retrieved documents from a source

    Args:
        user_query (str): User query
        notes (str): Content for answering the query
        queries (str): Previous queries
        vec_store (VectorStore): The vector store


    Returns:
        Tuple[str, str]: Tuple of queries and notes
    """

    # Persisted vector store
    vectordb = vec_store(
        persist_directory=persist_dir, embedding_function=embedding_function
    )

    # Create queries for brainstorming
    response = llm_chain_brainstorm_baseline(user_query, queries, notes, **kwargs)

    # Questions to be asked during search in json format
    questions = json.loads(response)
    top_questions = questions["queries"]

    compressed_contents = []
    # Loop through the relevant questions
    for i in tqdm(range(len(top_questions)), desc="BrainStorming"):
        question = top_questions[i]
        # Retrieve contents for a givent question from the source
        resources = vectordb.similarity_search(question)
        docs_resources = [resource.page_content for resource in resources]

        # Compress the contents of reranked documents
        compressed_content, _ = refine(docs_resources)
        compressed_contents.append(compressed_content)

    notes = f"{notes}\n\n SOURCE: \n NOTE: {compressed_contents}"
    queries = f"{queries}\n QUESTION: {top_questions}"

    return queries, notes

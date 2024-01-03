from typing import Optional

from langchain.schema import HumanMessage, SystemMessage

from prompts import (
    create_user_prompt_brainstorm,
    create_user_prompt_brainstorm_baseline,
    system_template_brainstorm,
)
from shared import chat_completions_with_backoff
from type_extensions import T


def llm_chain_brainstorm(
    user_query: str,
    queries: str,
    notes: str,
    chunks: Optional[str] = None,
    **kwargs: dict[str, T],
) -> str:
    """Function to use the LLM chain for brainstorming

    Args:
        user_query (str): User query
        queries (str): Previous queries
        notes (str): Content for answering the query
        chunks (str): Chunks of the document(s) from the vectorstore

    Returns:
        str: The text for response
    """
    user_message_brainstorm = create_user_prompt_brainstorm(
        user_query, queries, notes, chunks
    )

    # System and user prompts for brainstorming
    messages_brainstorm = [
        SystemMessage(content=system_template_brainstorm),
        HumanMessage(content=user_message_brainstorm),
    ]

    response = chat_completions_with_backoff(messages=messages_brainstorm, **kwargs)

    return response


def llm_chain_brainstorm_baseline(
    user_query: str,
    queries: str,
    notes: str,
    **kwargs: dict[str, T],
) -> str:
    """Function to use the LLM chain for brainstorming

    Args:
        user_query (str): User query
        queries (str): Previous queries
        notes (str): Content for answering the query


    Returns:
        str: The text for response
    """
    user_message_brainstorm = create_user_prompt_brainstorm_baseline(
        user_query, queries, notes
    )

    # System and user prompts for brainstorming
    messages_brainstorm = [
        SystemMessage(content=system_template_brainstorm),
        HumanMessage(content=user_message_brainstorm),
    ]

    response = chat_completions_with_backoff(messages=messages_brainstorm, **kwargs)

    return response

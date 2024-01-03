import json
from typing import Tuple

from langchain.schema import HumanMessage, SystemMessage

from prompts import create_user_prompt_satisfice, system_template_satisficing
from shared import chat_completions_with_backoff, get_cb
from type_extensions import T
from utils import custom_timer_with_return


@get_cb
@custom_timer_with_return
def satisfice(
    user_query: str,
    notes: str,
    queries: str,
    hypothesis: str,
    **kwargs: dict[str, T],
) -> Tuple[bool, str]:
    """Satisfice based on the provided information

    Args:
        user_query (str): User query
        notes (str): Content for answering the query
        queries (str): Previous queries
        hypothesis (str): Final hypothesis

    Returns:
        Tuple[bool, str]: Tuple of satisficed and feedback
    """
    user_message_satisfice = create_user_prompt_satisfice(
        user_query, notes, queries, hypothesis
    )

    # System and user prompts for satisficing
    messages_satisfice = [
        SystemMessage(content=system_template_satisficing),
        HumanMessage(content=user_message_satisfice),
    ]

    # LLM chain and response for satisficing
    response = chat_completions_with_backoff(messages=messages_satisfice, **kwargs)

    feedback = json.loads(response)

    return feedback["satisficed"], feedback["feedback"]

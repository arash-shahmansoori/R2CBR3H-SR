from langchain.schema import HumanMessage, SystemMessage

from prompts import create_user_prompt_hypothesis, system_template_hypothesis
from shared import chat_completions_with_backoff, get_cb
from type_extensions import T
from utils import custom_timer_with_return


@get_cb
@custom_timer_with_return
def hypothesize(
    user_query: str,
    notes: str,
    hypotheses: str,
    **kwargs: dict[str, T],
) -> str:
    """Hypothesize using the provided information

    Args:
        user_query (str): User query
        notes (str): Content for answering the query
        hypotheses (str): Previous hypothises

    Returns:
        str: Hypothesis response
    """
    user_message_hypothesis = create_user_prompt_hypothesis(
        user_query, notes, hypotheses
    )

    # System and user prompts for hypothesizing
    messages_hypothesize = [
        SystemMessage(content=system_template_hypothesis),
        HumanMessage(content=user_message_hypothesis),
    ]

    # LLM chain and response for hypothesizing
    response = chat_completions_with_backoff(messages=messages_hypothesize, **kwargs)

    return response

from langchain.schema import HumanMessage, SystemMessage

from prompts import create_user_prompt_refine, system_template_spr_refine
from shared import chat_completions_with_backoff, get_cb
from type_extensions import T
from utils import custom_timer_with_return


@get_cb
@custom_timer_with_return
def refine(notes: str, **kwargs: dict[str, T]) -> str:
    """Sparse prime representation of the notes

    Args:
        notes (str): Content for answering the query

    Returns:
        str: Sparse prime representation response
    """
    user_message_refine = create_user_prompt_refine(notes)

    # System and user prompts for refining
    messages_refine = [
        SystemMessage(content=system_template_spr_refine),
        HumanMessage(content=user_message_refine),
    ]

    # LLM and response for refining
    response = chat_completions_with_backoff(messages=messages_refine, **kwargs)

    return response

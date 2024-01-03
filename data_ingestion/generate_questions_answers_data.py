from typing import List, Tuple

from langchain.schema import HumanMessage, SystemMessage

from prompts import create_user_prompt_qa, system_template_qa
from shared import chat_completions_with_backoff, get_cb
from type_extensions import T
from utils import custom_timer_with_return


@get_cb
@custom_timer_with_return
def generate_qa_dataset(user_query: str, docs: List[str], **kwargs: dict[str, T]):
    """Generate questions and answers dataset

    Args:
        user_query (str): User query
        docs (List[str]): List of documents to generate questions and answers from

    Returns:
        Tuple[str, str]: Tuple of questions and answers
    """

    user_message = create_user_prompt_qa(user_query, docs)

    # System and user prompts for brainstorming
    messages_brainstorm = [
        SystemMessage(content=system_template_qa),
        HumanMessage(content=user_message),
    ]

    response = chat_completions_with_backoff(messages=messages_brainstorm, **kwargs)

    return response

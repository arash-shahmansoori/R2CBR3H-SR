import os
import random
import time
from typing import Callable, NoReturn

import dotenv
import openai
from langchain.chat_models import ChatOpenAI

from type_extensions import T

dotenv.load_dotenv()


chat_llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def retry_with_exponential_backoff(
    func: Callable[..., T],
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = (openai.RateLimitError,),
) -> Callable[..., Callable[..., T] | NoReturn]:
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs) -> Callable[..., T] | NoReturn:
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specific errors
            except errors as e:
                # Increment retries
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                time.sleep(delay)

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

    return wrapper


@retry_with_exponential_backoff
def chat_completions_with_backoff(*args, **kwargs) -> T:
    """Chat completion response with exponential backoff

    Returns:
        T: Response of the LLM chat of type Generic
    """
    return chat_llm(*args, **kwargs).content

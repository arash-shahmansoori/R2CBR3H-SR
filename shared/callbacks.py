import functools

from langchain.callbacks import get_openai_callback


def get_cb(func):
    @functools.wraps(func)
    def wrapper_get_cb(*args, **kwargs):
        with get_openai_callback() as cb:
            value = func(*args, **kwargs)
            if value:
                return value, cb
            return None, cb

    return wrapper_get_cb

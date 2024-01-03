import functools
from time import perf_counter


def custom_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t_start = perf_counter()
        func(*args, **kwargs)
        t_stop = perf_counter()

        td = t_stop - t_start
        return td

    return wrapper


def custom_timer_with_return(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t_start = perf_counter()
        out = func(*args, **kwargs)
        t_stop = perf_counter()

        td = t_stop - t_start
        return out, td

    return wrapper

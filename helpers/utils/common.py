from pathlib import Path
from functools import wraps
from datetime import datetime


def ensure_path(path):
    """Ensures that the full-path to the desired directory is created"""
    Path(path).mkdir(parents=True, exist_ok=True)


def measure_runtime(method):
    """
    Decorator that measures the runtime of the <method>.
    :param method: function to decorate.
    :type method: callable.
    :return: decorated function.
    """

    @wraps(method)
    def measure(*args, **kwargs):
        s = datetime.now()
        r = method(*args, **kwargs)
        f = datetime.now()
        d = (f - s)
        if d.microseconds > 0.0000:
            print(f"Execution of <{method.__name__}> finished (runtime): {d}")
        return r
    return measure

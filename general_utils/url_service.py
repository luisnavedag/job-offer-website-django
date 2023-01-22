from typing import Callable


def get_full_url(function: Callable) -> Callable:
    """
    The function is a wrapper for functions returning the path to a given resource from reverse.
    The function adds the used page address
    """
    def wrapper(self):
        reverse_url = function(self)
        return fr"http://127.0.0.1:8000{reverse_url}"
    return wrapper

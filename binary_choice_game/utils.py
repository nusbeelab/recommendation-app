from datetime import datetime
from random import shuffle
from typing import Any, Callable, List, TypeVar, Union


T = TypeVar("T")


def shuffle_new_list(lst: List[T]) -> List[T]:
    lst_copy = lst.copy()
    shuffle(lst_copy)
    return lst_copy


def try_else_none(success: Callable[[Any], T]) -> Union[T, None]:
    try:
        return success()
    except:
        return None


def timestamp2utcdatetime(timestamp_ms: Union[int, None]):
    return try_else_none(
        lambda: datetime.utcfromtimestamp(round(timestamp_ms / 1000))
    )

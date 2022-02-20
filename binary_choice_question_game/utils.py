from datetime import datetime
from random import shuffle
from typing import Any, Callable, TypeVar, Union


T = TypeVar("T")


def read_qns(filepath):
    return [tuple(row.split()) for row in open(filepath, "r")]


def shuffle_new_list(lst: list):
    lst_copy = lst.copy()
    shuffle(lst_copy)
    return lst_copy


def try_else_none(success: Callable[[Any], T]) -> Union[T, None]:
    try:
        return success()
    except:
        return None


def timestamp2datetime(timestamp_ms: Union[int, None]):
    return try_else_none(
        lambda: datetime.fromtimestamp(round(timestamp_ms / 1000))
    )

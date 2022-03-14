from abc import ABCMeta, abstractmethod
from enum import Enum
from random import random
from typing import Literal, Tuple, Optional

from binary_choice_game.models import Player

Treatment = Literal["NoR", "R_Random"]


class Recommender(metaclass=ABCMeta):
    @abstractmethod
    def rec(self, player: Player, options: Tuple[str, str]) -> Optional[bool]:
        pass


class NoneRecommender(Recommender):
    def rec(self, player: Player, options: Tuple[str, str]):
        return None


class RandomRecommender(Recommender):
    def rec(self, player: Player, options: Tuple[str, str]):
        return random() < 0.5


RECOMMENDER_HASHMAP = {
    "NoR": NoneRecommender(),
    "R_Random": RandomRecommender(),
}


def get_recommender(treatment: Treatment) -> Recommender:
    return RECOMMENDER_HASHMAP[treatment]

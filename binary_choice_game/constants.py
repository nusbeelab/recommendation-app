import json
import os
from typing import Dict, List, Tuple
import typing
from otree.api import BaseConstants

from binary_choice_game.recommendations import Treatment

config_filepath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "experimental_config",
)


def read_qns() -> List[Tuple[str, str]]:
    filepath = os.path.join(config_filepath, "binary_choice_questions.txt")
    with open(filepath, "r") as f:
        return [tuple(row.split()) for row in f]


def read_rec_algo_desc() -> Dict[Treatment, str]:
    filepath = os.path.join(config_filepath, "rec_algo_desc.json")
    with open(filepath, "r") as f:
        return {k: v for k, v in json.load(f).items()}


class C(BaseConstants):
    NAME_IN_URL = "binary_choice_game"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    QUESTIONS = read_qns()
    REC_ALGO_DESC = read_rec_algo_desc()
    NUM_TRIALS = len(QUESTIONS)
    TREATMENTS = typing.get_args(Treatment)

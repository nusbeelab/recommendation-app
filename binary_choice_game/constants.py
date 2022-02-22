import json
import os
from typing import Dict, List, Tuple
from otree.api import BaseConstants
from binary_choice_game.recommendations import RecOption

config_filepath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "experimental_config",
)


def read_qns() -> List[Tuple[str, str]]:
    filepath = os.path.join(config_filepath, "binary_choice_questions.txt")
    with open(filepath, "r") as f:
        return [tuple(row.split()) for row in f]


def read_rec_algo_desc() -> Dict[RecOption, str]:
    filepath = os.path.join(config_filepath, "rec_algo_desc.json")
    with open(filepath, "r") as f:
        return {
            k: v for k, v in json.load(f).items() if k in RecOption.__members__
        }


class C(BaseConstants):
    NAME_IN_URL = "binary_choice_game"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    QUESTIONS = read_qns()
    REC_ALGO_DESC = read_rec_algo_desc()
    NUM_TRIALS = len(QUESTIONS)
    TREATMENTS = list(RecOption.__members__)

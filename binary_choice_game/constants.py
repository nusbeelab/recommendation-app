import os
from otree.api import BaseConstants
from binary_choice_game.recommendations import RecOption

from binary_choice_game.utils import read_qns


class C(BaseConstants):
    NAME_IN_URL = "binary_choice_game"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    QUESTIONS = read_qns(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "binary_choice_questions.txt",
        )
    )
    NUM_TRIALS = len(QUESTIONS)

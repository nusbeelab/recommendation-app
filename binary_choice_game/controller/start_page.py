import logging
import random

from binary_choice_game.models import Player
from binary_choice_game.controller.game_page import GamePage


class StartPage(GamePage):
    @staticmethod
    def js_vars(player: Player):
        return dict(round_number=player.round_number)

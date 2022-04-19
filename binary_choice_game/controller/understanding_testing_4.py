from binary_choice_game.controller.common import is_assigned_rec_treatment
from binary_choice_game.controller.game_page import GamePage
from binary_choice_game.controller.recommendation import populate_rec_probas
from binary_choice_game.models import Player


class UnderstandingTesting4(GamePage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2 and is_assigned_rec_treatment(player)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        populate_rec_probas(player)

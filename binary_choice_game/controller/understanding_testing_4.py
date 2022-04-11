from binary_choice_game.controller.game_page import GamePage
from binary_choice_game.models import Player


class UnderstandingTesting4(GamePage):
    @staticmethod
    def is_displayed(player: Player):
        return (
            super(GamePage, GamePage).is_displayed(player)
            and player.round_number == 2
            and player.participant.treatment in ["R_Random", "R_Maj", "R_CF", "R_CBF"]
        )

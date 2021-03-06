from binary_choice_game.models import Player
from binary_choice_game.controller.common import is_assigned_rec_treatment
from binary_choice_game.controller.game_page import GamePage


class Stg3IntroPage2(GamePage):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.session.config.get("mode") == "experiment"
            and player.round_number == 3
            and is_assigned_rec_treatment(player)
        )

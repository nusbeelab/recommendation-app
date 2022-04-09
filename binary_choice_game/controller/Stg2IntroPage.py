from binary_choice_game.models import Player
from binary_choice_game.controller.GamePage import GamePage


class Stg2IntroPage(GamePage):
    @staticmethod
    def is_displayed(player: Player):
        return (
            # player.session.config.get("mode") == "experiment"
            # and
            player.round_number
            == 2
        )

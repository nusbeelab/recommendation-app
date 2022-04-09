from binary_choice_game.models import Player
from binary_choice_game.controller.RecommenderStore import recommenderStore
from binary_choice_game.controller.GamePage import GamePage


class EndPage(GamePage):
    @staticmethod
    def is_displayed(player: Player):
        return (
            super(GamePage, GamePage).is_displayed(player) and player.round_number == 3
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 3:
            recommenderStore.remove_recommender(player)

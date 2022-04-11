import logging
import random

from binary_choice_game.models import Player
from binary_choice_game.controller.game_page import GamePage


class StartPage(GamePage):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        logger = logging.getLogger(__name__)
        try:
            if player.round_number == 1:
                treatments = player.session.config.get("treatments")
                player.participant.treatment = random.choice(treatments)
                logger.info(
                    f"Participant {player.participant.code} is assigned treatment {player.participant.treatment}"
                )
        except Exception as err:
            logger.error(err)
            raise err

    @staticmethod
    def js_vars(player: Player):
        return dict(round_number=player.round_number)

import logging

from binary_choice_game.constants import C
from binary_choice_game.models import Player, Trial
from binary_choice_game.functions import get_data_export_row
from binary_choice_game.controller.GamePage import GamePage


class Results(GamePage):
    @staticmethod
    def vars_for_template(player: Player):
        logger = logging.getLogger(__name__)
        logger.info("Retrieving trial data for display.")
        try:
            trials = Trial.filter(player=player)
            trials = [
                {
                    header: data
                    for header, data in zip(
                        C.DATA_EXPORT_HEADERS, get_data_export_row(player, trial)
                    )
                }
                for trial in trials
            ]
            logger.info(f"Trials: {trials}")

            return dict(trials=trials)
        except Exception as err:
            logger.error(err)
            raise err

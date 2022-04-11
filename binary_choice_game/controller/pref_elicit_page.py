import logging
import random
from binary_choice_game.constants import C
from binary_choice_game.controller.common import is_assigned_rec_treatment
from binary_choice_game.controller.game_page import GamePage

from binary_choice_game.models import Player, PrefElicitTrial


def get_current_pref_elicit_trial(player: Player):
    return PrefElicitTrial.filter(player=player, response=None)[0]


def is_pref_elicit_finished(player: Player):
    return player.num_pref_elicit_completed >= C.NUM_PREF_ELICIT_TRIALS


class PrefElicitPage(GamePage):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.session.config.get("mode") == "experiment"
            and player.round_number == 3
            and is_assigned_rec_treatment(player)
        )

    @staticmethod
    def live_method(player: Player, data: dict):
        logger = logging.getLogger(__name__)
        logger.info(
            f"Received prefererence elicitation data from player {player.participant.code}: {data}."
        )
        try:
            if is_pref_elicit_finished(player):
                logger.info(
                    f"Preference elicitation for player {player.participant.code} is done."
                )
                return {player.id_in_group: dict(is_finished=True)}

            if data:
                logger.info(
                    f"Getting current trial for player {player.participant.code}."
                )
                trial = get_current_pref_elicit_trial(player)
                logger.info(f"Current trial: {trial}.")

                trial.response = data.get("response")
                player.num_pref_elicit_completed += 1
                logger.info(f"Recorded trial: {trial}")

            if is_pref_elicit_finished(player):
                logger.info(
                    f"Preference elicitation for player {player.participant.code} is done."
                )
                return {player.id_in_group: dict(is_finished=True)}

            logger.info(f"Getting next trial for player {player.participant.code}.")
            trial = get_current_pref_elicit_trial(player)
            logger.info(f"Next preference elicitation trial: {trial}")
            (
                left_option_value,
                right_option_value,
            ) = C.PREFERENCE_ELICITATION_PAYMENTS.get(trial.pref_elicit_problem_id)
            next_trial_data = {
                player.id_in_group: dict(
                    left_option_value=left_option_value,
                    right_option_value=right_option_value,
                    progress=player.num_pref_elicit_completed
                    / C.NUM_PREF_ELICIT_TRIALS,
                )
            }
            logger.info(
                f"Next preference elicitation trial data for player {player.participant.code}: {next_trial_data}"
            )

            return next_trial_data
        except Exception as err:
            logger.error(err)
            raise err

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.realized_pref_elicit_problem_id = (
            random.randrange(C.NUM_PREF_ELICIT_TRIALS) + 1
        )
        trial = PrefElicitTrial.filter(
            player=player, pref_elicit_problem_id=player.realized_pref_elicit_problem_id
        )[0]
        player.is_stg3_rec = not trial.response

        payment = C.PREFERENCE_ELICITATION_PAYMENTS.get(
            player.realized_pref_elicit_problem_id
        )[trial.response]
        player.stg3_payment = str(payment)

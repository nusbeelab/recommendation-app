import logging

from recommendation_data_toolbox.lottery import Lottery

from binary_choice_game.constants import C
from binary_choice_game.models import Player, Trial
from binary_choice_game.controller.game_page import GamePage


def get_current_trial(player: Player):
    return Trial.filter(player=player, button=None)[0]


def is_finished(player: Player):
    return player.num_completed == C.NUM_TRIALS_BY_STAGE[player.round_number]


def unpack_lottery(lot: Lottery):
    # sort by descending order
    order = lot.objective_consequences.argsort()[::-1]
    ocs = lot.objective_consequences[order]
    probs = lot.probs[order]
    return [
        # convert int and float to str to ensure that the data can be serialized
        dict(oc=str(oc), p=str(prob))
        for oc, prob in zip(ocs, probs)
    ]


class QnPage(GamePage):
    @staticmethod
    def live_method(player: Player, data: dict):
        logger = logging.getLogger(__name__)
        logger.info(f"Received data from player {player.participant.code}: {data}.")
        try:
            if is_finished(player):
                logger.info(f"Player {player.participant.code} has finished.")
                return {player.id_in_group: dict(is_finished=True)}

            if data:
                logger.info(
                    f"Getting current trial for player {player.participant.code}."
                )
                trial = get_current_trial(player)
                logger.info(f"Current trial: {trial}.")

                # trial.response = 0 if data.get("response") == 'L' and trial.
                trial.button = data.get("button")
                trial.start_str_timestamp_ms = str(data.get("start_timestamp_ms"))
                trial.end_str_timestamp_ms = str(data.get("end_timestamp_ms"))
                player.num_completed += 1
                logger.info(f"Recorded trial: {trial}")

            if is_finished(player):
                logger.info(f"Player {player.participant.code} has finished.")
                return {player.id_in_group: dict(is_finished=True)}

            logger.info(f"Getting next trial for player {player.participant.code}.")
            trial = get_current_trial(player)
            logger.info(f"Next trial: {trial}")

            problem = C.PROBLEM_MANAGER.convert_ids_to_problems([trial.problem_id])[0]
            left_option = unpack_lottery(problem.a)
            right_option = unpack_lottery(problem.b)
            if trial.left_option:
                left_option, right_option = right_option, left_option
            rec = (
                None
                if trial.rec_proba is None
                else "L"
                if (trial.rec_proba >= 0.5) == trial.left_option
                else "R"
            )
            next_trial_data = {
                player.id_in_group: dict(
                    left_option=left_option,
                    right_option=right_option,
                    rec=rec,
                    progress=player.num_completed
                    / C.NUM_TRIALS_BY_STAGE[player.round_number],
                )
            }
            logger.info(
                f"Next trial data for player {player.participant.code}: {next_trial_data}"
            )

            return next_trial_data
        except Exception as err:
            logger.error(err)
            raise err

import logging

from otree.common import get_app_label_from_import_path
from otree.api import Page

from binary_choice_game.constants import C
from binary_choice_game.functions import get_data_export_row
from binary_choice_game.models import Player, Trial

from recommendation_data_toolbox.lottery import Lottery


class GamePage(Page):
    def get_template_name(self):
        if self.template_name is not None:
            return self.template_name
        return "{}/views/{}.html".format(
            get_app_label_from_import_path(self.__module__),
            self.__class__.__name__,
        )


class StartPage(GamePage):
    pass


def get_current_trial(player: Player):
    try:
        return Trial.filter(player=player, button=None)[0]

    except Exception as err:
        logging.getLogger(__name__).error(err)
        raise err


def is_finished(player: Player):
    return player.num_completed == C.NUM_TRIALS_BY_STAGE[player.round_number]


def unpack_lottery(lot: Lottery):
    return [
        dict(oc=oc, p=prob) for oc, prob in zip(lot.objective_consequences, lot.probs)
    ]


class QnPage(GamePage):
    @staticmethod
    def live_method(player: Player, data: dict):
        logger = logging.getLogger(__name__)

        logger.info(f"Received data from player {player.id_in_group}: {data}.")

        if is_finished(player):
            logger.info(f"Player {player.id_in_group} has finished.")
            return {player.id_in_group: dict(is_finished=True)}

        if data:
            logger.info(f"Getting current trial for player {player.id_in_group}.")
            trial = get_current_trial(player)
            logger.info(f"Current trial: {trial}.")

            # trial.response = 0 if data.get("response") == 'L' and trial.
            trial.button = data.get("button")
            trial.start_str_timestamp_ms = str(data.get("start_timestamp_ms"))
            trial.end_str_timestamp_ms = str(data.get("end_timestamp_ms"))
            player.num_completed += 1
            logger.info(f"Recorded trial: {trial}")

        if is_finished(player):
            logger.info(f"Player {player.id_in_group} has finished.")
            return {player.id_in_group: dict(is_finished=True)}

        logger.info(f"Getting next trial for player {player.id_in_group}.")
        trial = get_current_trial(player)
        logger.info(f"Next trial: {trial}")

        # give recommendations here
        trial.rec = None

        lottery_pair = C.LOT_PAIR_MANAGER.convert_ids_to_lottery_pairs(
            [trial.problem_id]
        )[0]
        left_option = unpack_lottery(lottery_pair.a)
        right_option = unpack_lottery(lottery_pair.b)
        if trial.left_option == 1:
            left_option, right_option = right_option, left_option

        next_trial_data = {
            player.id_in_group: dict(
                left_option=left_option,
                right_option=right_option,
                rec=trial.rec,
                progress=player.num_completed
                / C.NUM_TRIALS_BY_STAGE[player.round_number],
            )
        }
        logger.info(
            f"Next trial data for player {player.id_in_group}: {next_trial_data}"
        )

        return next_trial_data


class EndPage(GamePage):
    @staticmethod
    def is_displayed(player: Player):
        return (
            super(GamePage, GamePage).is_displayed(player) and player.round_number == 3
        )


class Results(GamePage):
    @staticmethod
    def vars_for_template(player: Player):
        logger = logging.getLogger(__name__)
        logger.info("Retrieving trial data for display.")

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


PRE_EXPERIMENT_SEQ = [
    StartPage,
    QnPage,
    EndPage,
    # Results,
]

page_sequence = PRE_EXPERIMENT_SEQ

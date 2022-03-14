import logging
from binary_choice_game.constants import C
from binary_choice_game.models import Player, Trial
from otree.api import Page
from otree.common import get_app_label_from_import_path

from binary_choice_game.recommendations import NoneRecommender, get_recommender
from binary_choice_game.utils import timestamp2utcdatetime, try_else_none


class CustomPage(Page):
    def get_template_name(self):
        if self.template_name is not None:
            return self.template_name
        return "{}/views/{}.html".format(
            get_app_label_from_import_path(self.__module__),
            self.__class__.__name__,
        )


class StartPage(CustomPage):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(rec_algo_desc=C.REC_ALGO_DESC.get(player.treatment))


def get_current_trial(player: Player):
    try:
        trial = Trial.filter(player=player, response=None)[0]
        return trial

    except Exception as err:
        logging.getLogger(__name__).error(err)


def is_finished(player: Player):
    return player.num_completed == C.NUM_TRIALS


class QnPage(CustomPage):
    @staticmethod
    def live_method(player: Player, data: dict):
        logger = logging.getLogger(__name__)

        logger.info(f"Received data from player {player.id_in_group}: {data}.")

        if is_finished(player):
            logger.info(f"Player {player.id_in_group} has finished.")
            return {player.id_in_group: dict(is_finished=True)}

        if data:
            logger.info(
                f"Getting current trial for player {player.id_in_group}.")
            trial = get_current_trial(player)
            logger.info(f"Current trial: {trial}.")

            trial.response = data.get("response")
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

        recommender = get_recommender(player.treatment)
        if trial.rec == None and not isinstance(recommender, NoneRecommender):
            trial.rec = recommender.rec(player, (trial.optionA, trial.optionB))

        next_trial_data = {
            player.id_in_group: dict(
                optionA=trial.optionA,
                optionB=trial.optionB,
                rec=trial.rec,
            )
        }
        logger.info(
            f"Next trial for player {player.id_in_group}: {next_trial_data}")

        return next_trial_data


def get_derived_data(trial: Trial):
    rec = None if trial.rec == None else int(trial.rec)
    response = None if trial.response == None else int(trial.response)
    start_timestamp_ms = int(trial.start_str_timestamp_ms)
    end_timestamp_ms = int(trial.end_str_timestamp_ms)
    return {
        **trial.__dict__,
        **dict(
            rec=rec,
            response=response,
            utc_start_time=timestamp2utcdatetime(start_timestamp_ms),
            utc_end_time=timestamp2utcdatetime(end_timestamp_ms),
            time_spent_ms=try_else_none(
                lambda: end_timestamp_ms
                - start_timestamp_ms
            ),
        ),
    }


class Results(CustomPage):
    @staticmethod
    def vars_for_template(player: Player):
        logger = logging.getLogger(__name__)
        logger.info("Retrieving trial data for display.")

        trials = Trial.filter(player=player)
        trials = [get_derived_data(trial) for trial in trials]
        logger.info(f"Trials: {trials}")

        return dict(trials=trials)


page_sequence = [StartPage, QnPage, Results]

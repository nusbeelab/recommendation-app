import logging
import random
from typing import Dict, Type
import numpy as np

from otree.common import get_app_label_from_import_path
from otree.api import Page
from binary_choice_game.common import get_response

from binary_choice_game.constants import C
from binary_choice_game.functions import (
    generate_random_problem_id_list,
    get_data_export_row,
)
from binary_choice_game.models import Player, Trial

from recommendation_data_toolbox.lottery import Lottery
from recommendation_data_toolbox.rec import (
    Recommender,
    NoneRecommender,
    RandomRecommender,
    MostPopularChoiceRecommender,
)
from recommendation_data_toolbox.rec.content_based import (
    ContentBasedRandomForestRecommender,
)
from recommendation_data_toolbox.rec.cf.neighborhood_based import UbcfRecommender

from binary_choice_game.utils import get_rand_bool


class GamePage(Page):
    def get_template_name(self):
        if self.template_name is not None:
            return self.template_name
        return "{}/views/{}.html".format(
            get_app_label_from_import_path(self.__module__),
            self.__class__.__name__,
        )


RECOMMENDERS: Dict[str, Type[Recommender]] = dict()


def get_round1_response_data(player: Player):
    trials = Trial.filter(player=player.in_round(1))
    problem_ids = np.array([trial.problem_id for trial in trials])
    decisions = np.array([get_response(trial) for trial in trials])
    return problem_ids, decisions


class StartPage(GamePage):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        logger = logging.getLogger(__name__)
        if player.round_number == 1:
            treatments = player.session.config.get("treatments")
            player.participant.treatment = random.choice(treatments)
            logger.info(
                f"Participant {player.participant.code} is assigned treatment {player.participant.treatment}"
            )
        elif player.round_number == 2:
            treatment = player.participant.treatment
            if treatment == "NoR":
                RECOMMENDERS[player.participant.code] = NoneRecommender()
            elif treatment == "R_Random":
                RECOMMENDERS[player.participant.code] = RandomRecommender()
            elif treatment == "R_Maj":
                RECOMMENDERS[player.participant.code] = MostPopularChoiceRecommender()
            elif treatment == "R_CBF":
                problem_ids, decisions = get_round1_response_data(player)
                RECOMMENDERS[
                    player.participant.code
                ] = ContentBasedRandomForestRecommender(
                    problem_manager=C.PROBLEM_MANAGER,
                    subj_problem_ids=problem_ids,
                    subj_decisions=decisions,
                )
            elif treatment == "R_CF":
                # recommenders[player.participant.code] = UbcfRecommender()
                RECOMMENDERS[player.participant.code] = NoneRecommender
            else:
                raise ValueError()
        if player.round_number in [2, 3]:
            problem_ids = np.arange(60, 180)
            recs = RECOMMENDERS[player.participant.code].rec(problem_ids)
            for problem_id, rec in zip(problem_ids, recs):
                Trial.filter(player=player, problem_id=problem_id)[0].rec = rec

    @staticmethod
    def js_vars(player: Player):
        return dict(round_number=player.round_number)


def get_current_trial(player: Player):
    return Trial.filter(player=player, button=None)[0]


def is_finished(player: Player):
    return player.num_completed == C.NUM_TRIALS_BY_STAGE[player.round_number]


def unpack_lottery(lot: Lottery):
    # convert int and float to str to ensure that the data can be serialized
    return [
        dict(oc=str(oc), p=str(prob))
        for oc, prob in zip(lot.objective_consequences, lot.probs)
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
                f"Next trial data for player {player.participant.code}: {next_trial_data}"
            )

            return next_trial_data
        except Exception as err:
            logger.info("wtf")
            logger.error(err)
            raise err


class EndPage(GamePage):
    @staticmethod
    def is_displayed(player: Player):
        return (
            super(GamePage, GamePage).is_displayed(player) and player.round_number == 3
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 3:
            del RECOMMENDERS[player.participant.code]


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


PRE_EXPERIMENT_SEQ = [
    StartPage,
    QnPage,
    EndPage,
    # Results,
]

page_sequence = PRE_EXPERIMENT_SEQ

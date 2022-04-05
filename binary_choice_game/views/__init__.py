import logging
import random

from otree.common import get_app_label_from_import_path
from otree.api import Page

from recommendation_data_toolbox.lottery import Lottery

from binary_choice_game.constants import C
from binary_choice_game.functions import get_data_export_row
from binary_choice_game.models import Player, Trial
from binary_choice_game.views.RecommenderStore import RecommenderStore


class GamePage(Page):
    def get_template_name(self):
        if self.template_name is not None:
            return self.template_name
        return "{}/views/{}.html".format(
            get_app_label_from_import_path(self.__module__),
            self.__class__.__name__,
        )


recommenderStore = RecommenderStore()


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
            elif player.round_number == 2:
                recommenderStore.intialize_recommender(player)
                logger.info(
                    f"{type(recommenderStore.get_recommender(player)).__name__} has been initialized for participant {player.participant.code}"
                )
            if player.round_number in [2, 3]:
                problem_ids = C.QUESTIONS_DF_BY_STAGE[player.round_number][
                    "id"
                ].to_numpy()
                recs = recommenderStore.get_recommender(player).rec(problem_ids)
                logger.info(
                    f"Participant {player.participant.code} is given the following recommendations for problems {problem_ids}: {recs}"
                )
                trials = Trial.filter(player=player)
                for problem_id, rec in zip(problem_ids, recs):
                    trial = next(
                        trial for trial in trials if trial.problem_id == problem_id
                    )
                    trial.rec = rec
        except Exception as err:
            logger.error(err)

    @staticmethod
    def js_vars(player: Player):
        return dict(round_number=player.round_number)


class Stg2IntroPage(GamePage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


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
            rec = (
                None
                if trial.rec is None
                else "L"
                if trial.rec == trial.left_option
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
    Stg2IntroPage,
    QnPage,
    EndPage,
    # Results,
]

page_sequence = PRE_EXPERIMENT_SEQ

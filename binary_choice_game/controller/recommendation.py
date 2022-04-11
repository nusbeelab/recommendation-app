import logging
from typing import Dict, Type
import numpy as np

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
from binary_choice_game.constants import C
from binary_choice_game.controller.common import is_assigned_rec_treatment

from binary_choice_game.models import Player, Trial
from binary_choice_game.utils import get_response


def get_round1_response_data(player: Player):
    trials = Trial.filter(player=player.in_round(1))
    problem_ids = np.array([trial.problem_id for trial in trials])
    decisions = np.array(
        [get_response(trial.button, trial.left_option) for trial in trials]
    )
    return problem_ids, decisions


class RecommenderStore:
    def __init__(self):
        self.store: Dict[str, Type[Recommender]] = dict()

    def intialize_recommender(self, player: Player):
        if player.participant.code in self.store:
            return
        treatment = player.participant.treatment
        if treatment == "NoR":
            recommender = NoneRecommender()
        elif treatment == "R_Random":
            recommender = RandomRecommender()
        elif treatment == "R_Maj":
            recommender = MostPopularChoiceRecommender()
        elif treatment == "R_CBF":
            problem_ids, decisions = get_round1_response_data(player)
            recommender = ContentBasedRandomForestRecommender(
                problem_manager=C.PROBLEM_MANAGER,
                subj_problem_ids=problem_ids,
                subj_decisions=decisions,
            )
        elif treatment == "R_CF":
            problem_ids, decisions = get_round1_response_data(player)
            recommender = UbcfRecommender(
                rating_matrix=C.PREEXPERIMENT_RATING_MATRIX,
                subj_problem_ids=problem_ids,
                subj_decisions=decisions,
            )
        else:
            raise ValueError()
        self.store[player.participant.code] = recommender

    def get_recommender(self, player: Player):
        if player.participant.code not in self.store:
            self.intialize_recommender(player)
        if (
            player.round_number == 3
            and is_assigned_rec_treatment(player)
            and not player.is_stg3_rec
        ):
            return NoneRecommender()
        return self.store[player.participant.code]

    def remove_recommender(self, player: Player):
        self.store.pop(player.participant.code, None)


recommenderStore = RecommenderStore()


def generate_recommendations(player: Player):
    logger = logging.getLogger(__name__)
    try:
        recommenderStore.intialize_recommender(player)
        logger.info(
            f"{type(recommenderStore.get_recommender(player)).__name__} has been initialized for participant {player.participant.code}"
        )
        problem_ids = C.QUESTIONS_DF_BY_STAGE[player.round_number]["id"].to_numpy()
        recs = recommenderStore.get_recommender(player).rec(problem_ids)
        logger.info(
            f"Participant {player.participant.code} is given the following recommendations for problems {problem_ids}: {recs}"
        )
        trials = Trial.filter(player=player)
        for problem_id, rec in zip(problem_ids, recs):
            trial = next(trial for trial in trials if trial.problem_id == problem_id)
            trial.rec = rec
    except Exception as err:
        logger.error(err)
        raise err

import logging
import random

from binary_choice_game.constants import C
from binary_choice_game.models import Player, Trial
from binary_choice_game.controller.RecommenderStore import recommenderStore
from binary_choice_game.controller.GamePage import GamePage


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
            raise err

    @staticmethod
    def js_vars(player: Player):
        return dict(round_number=player.round_number)

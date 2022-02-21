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
    return Trial.filter(player=player, response=None)[0]


def is_finished(player: Player):
    return player.num_completed == C.NUM_TRIALS


class QnPage(CustomPage):
    @staticmethod
    def live_method(player: Player, data: dict):
        if is_finished(player):
            return {player.id_in_group: dict(is_finished=True)}

        if data:
            trial = get_current_trial(player)
            trial.response = data.get("response")
            trial.start_timestamp_ms = data.get("start_timestamp_ms")
            trial.end_timestamp_ms = data.get("end_timestamp_ms")
            player.num_completed += 1

        if is_finished(player):
            return {player.id_in_group: dict(is_finished=True)}

        trial = get_current_trial(player)
        recommender = get_recommender(player.treatment)
        if trial.rec == None and not isinstance(recommender, NoneRecommender):
            trial.rec = recommender.rec(player, (trial.optionA, trial.optionB))
        return {
            player.id_in_group: dict(
                optionA=trial.optionA,
                optionB=trial.optionB,
                rec=trial.rec,
            )
        }


class Results(CustomPage):
    @staticmethod
    def vars_for_template(player: Player):
        trials = Trial.filter(player=player)
        trials = [
            {
                **trial.__dict__,
                **dict(
                    rec=None if trial.rec == None else int(trial.rec),
                    response=None
                    if trial.response == None
                    else int(trial.response),
                    utc_start_time=timestamp2utcdatetime(
                        trial.start_timestamp_ms
                    ),
                    utc_end_time=timestamp2utcdatetime(trial.end_timestamp_ms),
                    time_spent_ms=try_else_none(
                        lambda: trial.end_timestamp_ms
                        - trial.start_timestamp_ms
                    ),
                ),
            }
            for trial in trials
        ]
        return dict(trials=trials)


page_sequence = [StartPage, QnPage, Results]

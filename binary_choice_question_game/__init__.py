import os
from random import random
from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    ExtraModel,
    Page,
)

from binary_choice_question_game.utils import (
    read_qns,
    shuffle_new_list,
    timestamp2utcdatetime,
    try_else_none,
)

doc = """
Binary choice questions
"""


class C(BaseConstants):
    NAME_IN_URL = "NoR"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    QUESTIONS = read_qns(os.path.join(__name__, "binary_choice_questions.txt"))
    NUM_TRIALS = len(QUESTIONS)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_completed = models.IntegerField(initial=0)


class Trial(ExtraModel):
    player = models.Link(Player)
    optionA = models.StringField()
    optionB = models.StringField()
    response = (
        models.BooleanField()
    )  # False (0) corresponds to optionA, True (1) corresponds to optionB
    start_timestamp_ms = models.IntegerField()
    end_timestamp_ms = models.IntegerField()


# HELPER FUNCTIONS
def get_current_trial(player: Player):
    return Trial.filter(player=player, response=None)[0]


def is_finished(player: Player):
    return player.num_completed == C.NUM_TRIALS


# FUNCTIONS
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        for qn in shuffle_new_list(C.QUESTIONS):
            optionA, optionB = qn if random() < 0.5 else qn[::-1]
            Trial.create(player=player, optionA=optionA, optionB=optionB)


def live_method(player: Player, data: dict):
    if data:
        trial = get_current_trial(player)
        trial.response = data.get("response")
        trial.start_timestamp_ms = data.get("start_timestamp_ms")
        trial.end_timestamp_ms = data.get("end_timestamp_ms")
        player.num_completed += 1

    if is_finished(player):
        return {player.id_in_group: dict(is_finished=True)}

    trial = get_current_trial(player)
    return {
        player.id_in_group: dict(optionA=trial.optionA, optionB=trial.optionB)
    }


# PAGES
class QnPage(Page):
    live_method = live_method


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(trials=Trial.filter(player=player))


page_sequence = [QnPage, Results]


# DATA EXPORT
def custom_export(players):
    # header row
    yield [
        "session",
        "participant_code",
        "optionA",
        "optionB",
        "response",
        "utc_start_time",
        "utc_end_time",
        "time_spent_ms",
    ]
    for p in players:
        participant = p.participant
        session = p.session
        for trial in Trial.filter(player=p):
            yield [
                session.code,
                participant.code,
                trial.optionA,
                trial.optionB,
                trial.response,
                timestamp2utcdatetime(trial.start_timestamp_ms),
                timestamp2utcdatetime(trial.end_timestamp_ms),
                try_else_none(
                    lambda: trial.end_timestamp_ms - trial.start_timestamp_ms
                ),
            ]

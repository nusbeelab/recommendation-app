from typing import List
from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    ExtraModel,
    Page,
)
from random import shuffle
import os

doc = """
Binary choice questions
"""


def read_qns():
    return [
        tuple(row.split())
        for row in open(
            os.path.join(__name__, "binary_choice_questions.txt"), "r"
        )
    ]


class C(BaseConstants):
    NAME_IN_URL = "NoR"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    QUESTIONS = read_qns()
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


# HELPER FUNCTIONS
def get_shuffled_questions():
    questions = C.QUESTIONS.copy()
    shuffle(questions)
    return questions


def get_current_trial(player: Player):
    return Trial.filter(player=player, response=None)[0]


def is_finished(player: Player):
    return player.num_completed == C.NUM_TRIALS


# FUNCTIONS
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        for qn in get_shuffled_questions():
            Trial.create(player=player, optionA=qn[0], optionB=qn[1])


def live_method(player: Player, data: dict):
    if data:
        trial = get_current_trial(player)
        trial.response = data.get("response")
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


def custom_export(players):
    # header row
    yield [
        "session",
        "participant_code",
        "optionA",
        "optionB",
        "response",
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
            ]

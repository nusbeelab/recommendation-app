from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page


class C(BaseConstants):
    NAME_IN_URL = "end"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


page_sequence = []

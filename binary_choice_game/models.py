from otree.api import (
    models,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    ExtraModel,
)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
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

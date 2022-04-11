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
    num_completed = models.IntegerField(initial=0)
    num_pref_elicit_completed = models.IntegerField(initial=0)
    realized_pref_elicit_problem_id = models.IntegerField()
    is_stg3_rec = models.BooleanField()
    stg3_payment = models.StringField()


class Trial(ExtraModel):
    player = models.Link(Player)
    problem_id = models.IntegerField()
    # False (0) corresponds to optionA, True (1) corresponds to optionB
    left_option = models.BooleanField()
    rec = models.BooleanField()
    button = models.StringField()
    # use string to store timestamps to avoid psycopg2.errors.NumericValueOutOfRange
    start_str_timestamp_ms = models.StringField()
    end_str_timestamp_ms = models.StringField()


class PrefElicitTrial(ExtraModel):
    player = models.Link(Player)
    pref_elicit_problem_id = models.IntegerField()
    # False (0) corresponds to optionA, True (1) corresponds to optionB
    response = models.BooleanField()

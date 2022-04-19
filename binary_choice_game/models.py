from otree.api import (
    models,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    ExtraModel,
)

from binary_choice_game.constants import C


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def with_pref_response_fields(cls):
    for i in range(1, C.NUM_PREF_ELICIT_TRIALS + 1):
        setattr(cls, f"pref_{i}", models.BooleanField())
    return cls


@with_pref_response_fields
class Player(BasePlayer):
    num_completed = models.IntegerField(initial=0)
    cur_pref_elicit_problem_id = models.IntegerField(initial=1)
    realized_pref_elicit_problem_id = models.IntegerField()
    is_stg3_rec = models.BooleanField()
    stg3_payment = models.StringField()


class Trial(ExtraModel):
    player = models.Link(Player)
    problem_id = models.IntegerField()
    # False (0) corresponds to optionA, True (1) corresponds to optionB
    left_option = models.BooleanField()
    rec_proba = models.FloatField()
    button = models.StringField()
    # use string to store timestamps to avoid psycopg2.errors.NumericValueOutOfRange
    start_str_timestamp_ms = models.StringField()
    end_str_timestamp_ms = models.StringField()

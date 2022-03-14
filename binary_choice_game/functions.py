import logging
import random
from binary_choice_game import C
from binary_choice_game.models import Subsession, Trial
from binary_choice_game.recommendations import Treatment
from binary_choice_game.utils import (
    get_rand_bool,
    shuffle_new_list,
    timestamp2utcdatetime,
    try_else_none,
)


def creating_session(subsession: Subsession):
    logger = logging.getLogger(__name__)
    treatment = subsession.session.config.get("name")
    logger.info(f"Session treatment: {treatment}")

    for player in subsession.get_players():
        player.treatment = (
            treatment
            if treatment in C.TREATMENTS
            else random.choice(C.TREATMENTS)
        )
        for qn in shuffle_new_list(C.QUESTIONS):
            optionA, optionB = qn if get_rand_bool() else qn[::-1]
            Trial.create(player=player, optionA=optionA, optionB=optionB)


def custom_export(players):
    # header row
    yield [
        "session",
        "participant_code",
        "treatment",
        "optionA",
        "optionB",
        "recommendation",
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
                p.treatment,
                trial.optionA,
                trial.optionB,
                trial.rec,
                trial.response,
                timestamp2utcdatetime(trial.start_timestamp_ms),
                timestamp2utcdatetime(trial.end_timestamp_ms),
                try_else_none(
                    lambda: trial.end_timestamp_ms - trial.start_timestamp_ms
                ),
            ]

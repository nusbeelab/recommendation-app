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

    try:
        for player in subsession.get_players():
            player.treatment = (
                treatment
                if treatment in C.TREATMENTS
                else random.choice(C.TREATMENTS)
            )
            for qn in shuffle_new_list(C.QUESTIONS):
                optionA, optionB = qn if get_rand_bool() else qn[::-1]
                Trial.create(player=player, optionA=optionA, optionB=optionB)
    except Exception as err:
        logger.error(err)


def custom_export(players):
    logger = logging.getLogger(__name__)
    
    logger.info("Executing custom data export.")

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
    try:
        for p in players:
            participant = p.participant
            session = p.session
            for trial in Trial.filter(player=p):
                start_timestamp_ms = int(trial.start_str_timestamp_ms)
                end_timestamp_ms = int(trial.end_str_timestamp_ms)
                yield [
                    session.code,
                    participant.code,
                    p.treatment,
                    trial.optionA,
                    trial.optionB,
                    trial.rec,
                    trial.response,
                    timestamp2utcdatetime(start_timestamp_ms),
                    timestamp2utcdatetime(end_timestamp_ms),
                    try_else_none(
                        lambda: end_timestamp_ms - start_timestamp_ms
                    ),
                ]
    except Exception as err:
        logger.error(err)

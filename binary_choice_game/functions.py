import random
from binary_choice_game import C
from binary_choice_game.models import Player, Subsession, Trial
from binary_choice_game.utils import (
    shuffle_new_list,
    timestamp2utcdatetime,
    try_else_none,
)


def get_current_trial(player: Player):
    return Trial.filter(player=player, response=None)[0]


def is_finished(player: Player):
    return player.num_completed == C.NUM_TRIALS


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        for qn in shuffle_new_list(C.QUESTIONS):
            optionA, optionB = qn if random.random() < 0.5 else qn[::-1]
            Trial.create(player=player, optionA=optionA, optionB=optionB)


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
    return {
        player.id_in_group: dict(optionA=trial.optionA, optionB=trial.optionB)
    }


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

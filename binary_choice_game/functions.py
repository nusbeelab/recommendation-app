from itertools import permutations
import logging
import random
from typing import Iterable, List

from binary_choice_game import C
from binary_choice_game.utils import get_response
from binary_choice_game.models import Player, Subsession, Trial
from binary_choice_game.utils import (
    get_rand_bool,
    timestamp2utcdatetime,
    try_else_none,
)

DATA_EXPORT_HEADERS = [
    "session_code",
    "participant_code",
    "treatment",
    "problem_id",
    "stage",
    "problem",
    "xa1",
    "pa1",
    "xa2",
    "pa2",
    "xa3",
    "pa3",
    "xb1",
    "pb1",
    "xb2",
    "pb2",
    "xb3",
    "pb3",
    "left_option",
    "rec_proba",
    "button",
    "response",
    "utc_start_time",
    "utc_end_time",
    "time_spent_ms",
]


def generate_random_problem_id_list(stage: int):
    return C.QUESTIONS_DF_BY_STAGE[stage]["id"].sample(frac=1).to_list()


def treatment_assignment(treatments: List[str], treatment_block_size: int):
    if treatment_block_size % len(treatments) != 0:
        raise ValueError(
            f"The block size ({treatment_block_size}) is not a multiple of the number of treatments ({len(treatments)})"
        )
    sample_treatment_block = treatments * (treatment_block_size // len(treatments))
    treatment_blocks = list(permutations(sample_treatment_block))

    cur_treatment_block = None
    cur_idx = len(treatment_blocks)

    while True:
        if cur_idx >= treatment_block_size:
            cur_treatment_block = random.choice(treatment_blocks)
            cur_idx = 0
        yield cur_treatment_block[cur_idx]
        cur_idx += 1


def creating_session(subsession: Subsession):
    logger = logging.getLogger(__name__)
    try:
        treatments = subsession.session.config.get("treatments")
        treatment_gen = treatment_assignment(treatments, C.TREATMENT_BLOCK_SIZE)
        for player in subsession.get_players():
            if subsession.round_number == 1:
                player.participant.treatment = next(treatment_gen)
                logger.info(
                    f"Participant {player.participant.code} is assigned treatment {player.participant.treatment}"
                )

            for id in generate_random_problem_id_list(player.round_number):
                Trial.create(player=player, problem_id=id, left_option=get_rand_bool())

    except Exception as err:
        logger.error(err)


def get_data_export_row(player: Player, trial: Trial):
    try:
        qns_df = C.QUESTIONS_DF_BY_STAGE[player.round_number]
        df_row = qns_df[qns_df["id"] == trial.problem_id].iloc[0]
        params_from_df = df_row[
            [
                "stage",
                "problem",
                "xa1",
                "pa1",
                "xa2",
                "pa2",
                "xa3",
                "pa3",
                "xb1",
                "pb1",
                "xb2",
                "pb2",
                "xb3",
                "pb3",
            ]
        ]
        response = get_response(trial.button, trial.left_option)
        start_timestamp_ms = int(trial.start_str_timestamp_ms or 0)
        end_timestamp_ms = int(trial.end_str_timestamp_ms or 0)
        rec_proba = f"{trial.rec_proba:5f}" if trial.rec_proba is not None else None
        return (
            [
                player.session.code,
                player.participant.code,
                player.participant.vars.get("treatment"),  # nullable
                trial.problem_id,
            ]
            + list(params_from_df)
            + [
                trial.left_option,
                rec_proba,
                trial.button,
                response,
                timestamp2utcdatetime(start_timestamp_ms),
                timestamp2utcdatetime(end_timestamp_ms),
                try_else_none(lambda: end_timestamp_ms - start_timestamp_ms),
            ]
        )
    except Exception as err:
        logging.getLogger(__name__).error(err)
        raise err


def custom_export(players: Iterable[Player]):
    logger = logging.getLogger(__name__)

    logger.info("Exporting data.")

    # header row
    yield DATA_EXPORT_HEADERS
    try:
        for p in players:
            for trial in Trial.filter(player=p):
                yield get_data_export_row(p, trial)
    except Exception as err:
        logger.error(err)

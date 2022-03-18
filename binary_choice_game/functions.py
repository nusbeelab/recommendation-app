import logging
import random
from typing import Iterable
from binary_choice_game import C
from binary_choice_game.models import Player, Subsession, Trial
from binary_choice_game.utils import (
    get_rand_bool,
    timestamp2utcdatetime,
    try_else_none,
)


def generate_random_problem_id_list():
    stages = list(C.QUESTION_DF["stage"].unique())
    df = C.QUESTION_DF.sample(frac=1)
    return [id for stage in stages for id in df["id"][df["stage"] == stage]]


def creating_session(subsession: Subsession):
    logger = logging.getLogger(__name__)
    treatment = subsession.session.config.get("name")
    logger.info(f"Session treatment: {treatment}")

    try:
        for player in subsession.get_players():
            player.treatment = (
                treatment if treatment in C.TREATMENTS else random.choice(C.TREATMENTS)
            )
            for id in generate_random_problem_id_list():
                Trial.create(player=player, problem_id=id, left_option=get_rand_bool())
    except Exception as err:
        logger.error(err)


def get_data_export_row(player: Player, trial: Trial):
    try:
        df_row = C.QUESTION_DF[C.QUESTION_DF["id"] == trial.problem_id].iloc[0]
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
        response = trial.left_option if trial.button == "L" else not trial.left_option
        start_timestamp_ms = int(trial.start_str_timestamp_ms or 0)
        end_timestamp_ms = int(trial.end_str_timestamp_ms or 0)
        return (
            [
                player.session.code,
                player.participant.code,
                player.treatment,
                trial.problem_id,
            ]
            + list(params_from_df)
            + [
                trial.rec,
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
    yield C.DATA_EXPORT_HEADERS
    try:
        for p in players:
            for trial in Trial.filter(player=p):
                yield get_data_export_row(p, trial)
    except Exception as err:
        logger.error(err)

import logging
import random
from typing import Iterable, Literal, Optional
from binary_choice_game import C
from binary_choice_game.models import Player, Subsession, Trial
from binary_choice_game.utils import (
    get_rand_bool,
    timestamp2utcdatetime,
    try_else_none,
)


def generate_random_problem_id_list(stage: int):
    return C.QUESTIONS_DF_BY_STAGE[stage]["id"].sample(frac=1).to_list()


def creating_session(subsession: Subsession):
    logger = logging.getLogger(__name__)
    treatment = subsession.session.config.get("treatment")
    logger.info(f"Session treatment: {treatment}")

    try:
        for player in subsession.get_players():
            for id in generate_random_problem_id_list(player.round_number):
                Trial.create(player=player, problem_id=id, left_option=get_rand_bool())
            player.participant.treatment = (
                treatment if treatment in C.TREATMENTS else random.choice(C.TREATMENTS)
            )
    except Exception as err:
        logger.error(err)


def get_response(button: Optional[Literal["L", "R"]], left_option: bool):
    if button == None:
        return None
    if button == "L":
        return left_option
    if button == "R":
        return not left_option
    raise ValueError("Value of button must be 'L' or 'R' or None")


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
        return (
            [
                player.session.code,
                player.participant.code,
                player.treatment,
                trial.problem_id,
            ]
            + list(params_from_df)
            + [
                trial.left_option,
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

import json
import os
import pandas as pd

from typing import Any, Dict

from otree.api import BaseConstants

from recommendation_data_toolbox.lottery import get_problem_manager

from settings import QUESTIONS_CSV_FILE

config_filepath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "experimental_config",
)


def read_qns_by_stage() -> Dict[int, pd.DataFrame]:
    filepath = os.path.join(config_filepath, QUESTIONS_CSV_FILE)
    return dict(
        tuple(pd.read_csv(filepath).rename_axis("id").reset_index().groupby("stage"))
    )


def get_num_trials_by_stage(dfs: Dict[Any, pd.DataFrame]):
    return {k: len(v) for k, v in dfs.items()}


def read_rec_algo_desc() -> Dict[str, str]:
    filepath = os.path.join(config_filepath, "rec_algo_desc.json")
    with open(filepath, "r") as f:
        return {k: v for k, v in json.load(f).items()}


class C(BaseConstants):
    NAME_IN_URL = "gamble"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    QUESTIONS_DF_BY_STAGE = read_qns_by_stage()
    PROBLEM_MANAGER = get_problem_manager(pd.concat(QUESTIONS_DF_BY_STAGE.values()))
    NUM_TRIALS_BY_STAGE = get_num_trials_by_stage(QUESTIONS_DF_BY_STAGE)
    REC_ALGO_DESC = read_rec_algo_desc()
    PREEXPERIMENT_RATING_MATRIX = (None,)
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
        "recommendation",
        "button",
        "response",
        "utc_start_time",
        "utc_end_time",
        "time_spent_ms",
    ]

import json
import os
import pandas as pd

from typing import Any, Dict

from otree.api import BaseConstants

from recommendation_data_toolbox.lottery import get_problem_manager

from binary_choice_game.utils import get_response
from settings import QUESTIONS_CSV_FILE

resources_filepath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "resources",
)


def read_qns_by_stage() -> Dict[int, pd.DataFrame]:
    filepath = os.path.join(resources_filepath, QUESTIONS_CSV_FILE)
    return dict(
        tuple(pd.read_csv(filepath).rename_axis("id").reset_index().groupby("stage"))
    )


def get_num_trials_by_stage(dfs: Dict[Any, pd.DataFrame]):
    return {k: len(v) for k, v in dfs.items()}


def read_rec_algo_desc() -> Dict[str, str]:
    filepath = os.path.join(resources_filepath, "rec_algo_desc.json")
    with open(filepath, "r") as f:
        return {k: v for k, v in json.load(f).items()}


def convert_subj_data_to_rating_vector(subj_df: pd.DataFrame):
    decisions = subj_df["decision"].to_list()
    problem_ids = subj_df["problem_id"].to_list()
    assert len(decisions) == 180
    assert len(problem_ids) == 180
    problem_ids, decisions = zip(*sorted(zip(problem_ids, decisions)))
    return pd.Series(decisions, index=problem_ids, name=subj_df.index[0])


def get_preexperiment_rating_matrix():
    df = pd.read_csv(os.path.join(resources_filepath, "preexperiment_data.csv"))
    assert len(df) == 180 * 446
    return (
        df.groupby("participant_code").apply(convert_subj_data_to_rating_vector).values
    )


class C(BaseConstants):
    NAME_IN_URL = "gamble"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    QUESTIONS_DF_BY_STAGE = read_qns_by_stage()
    PROBLEM_MANAGER = get_problem_manager(pd.concat(QUESTIONS_DF_BY_STAGE.values()))
    NUM_TRIALS_BY_STAGE = get_num_trials_by_stage(QUESTIONS_DF_BY_STAGE)
    REC_ALGO_DESC = read_rec_algo_desc()
    PREEXPERIMENT_RATING_MATRIX = get_preexperiment_rating_matrix()
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

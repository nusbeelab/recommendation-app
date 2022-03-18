import json
import os
from typing import Any, Dict
import typing
import numpy as np
from otree.api import BaseConstants
import pandas as pd

from recommendation_data_toolbox.lottery import Lottery, LotteryPair, LotteryPairManager

from binary_choice_game.recommendations import Treatment

config_filepath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "experimental_config",
)


def read_qns_by_stage() -> Dict[int, pd.DataFrame]:
    filepath = os.path.join(config_filepath, "parameters_15Mar2022.csv")
    return dict(
        tuple(pd.read_csv(filepath).rename_axis("id").reset_index().groupby("stage"))
    )


def map_question_param_to_lot_pair(row: pd.Series):
    lot_a = Lottery(
        np.array(row[["xa1", "xa2", "xa3"]]), np.array(row[["pa1", "pa2", "pa3"]])
    )
    lot_b = Lottery(
        np.array(row[["xb1", "xb2", "xb3"]]), np.array(row[["pb1", "pb2", "pb3"]])
    )
    return LotteryPair(lot_a, lot_b)


def get_lot_pair_manager(df: pd.DataFrame):
    lot_pairs = list(df.apply(map_question_param_to_lot_pair, axis=1))
    return LotteryPairManager(lot_pairs=lot_pairs)


def get_num_trials_by_stage(dfs: Dict[Any, pd.DataFrame]):
    return {k: len(v) for k, v in dfs.items()}


def read_rec_algo_desc() -> Dict[Treatment, str]:
    filepath = os.path.join(config_filepath, "rec_algo_desc.json")
    with open(filepath, "r") as f:
        return {k: v for k, v in json.load(f).items()}


class C(BaseConstants):
    NAME_IN_URL = "gamble"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    QUESTIONS_DF_BY_STAGE = read_qns_by_stage()
    LOT_PAIR_MANAGER = get_lot_pair_manager(pd.concat(QUESTIONS_DF_BY_STAGE.values()))
    NUM_TRIALS_BY_STAGE = get_num_trials_by_stage(QUESTIONS_DF_BY_STAGE)
    REC_ALGO_DESC = read_rec_algo_desc()
    TREATMENTS = typing.get_args(Treatment)
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
        "recommendation",
        "button",
        "response",
        "utc_start_time",
        "utc_end_time",
        "time_spent_ms",
    ]

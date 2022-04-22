import os
import pandas as pd

from typing import Any, Dict

from otree.api import BaseConstants

from recommendation_data_toolbox.lottery import get_problem_manager


QUESTIONS_CSV_FILE = "parameters_2Apr2022.csv"
PREFERENCE_ELICITATION_CSV_FILE = "preference_elicitation_220403.csv"

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


def get_preference_elicitation_payments():
    df = pd.read_csv(os.path.join(resources_filepath, PREFERENCE_ELICITATION_CSV_FILE))
    return {
        row["elicitation_problem"]: (row["optionA_payment"], row["optionB_payment"])
        for _, row in df.iterrows()
    }


class C(BaseConstants):
    NAME_IN_URL = "gamble"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    TREATMENT_BLOCK_SIZE = 10
    QUESTIONS_DF_BY_STAGE = read_qns_by_stage()
    PROBLEM_MANAGER = get_problem_manager(pd.concat(QUESTIONS_DF_BY_STAGE.values()))
    NUM_TRIALS_BY_STAGE = get_num_trials_by_stage(QUESTIONS_DF_BY_STAGE)
    PREEXPERIMENT_RATING_MATRIX = get_preexperiment_rating_matrix()
    PREFERENCE_ELICITATION_PAYMENTS = get_preference_elicitation_payments()
    NUM_PREF_ELICIT_TRIALS = len(PREFERENCE_ELICITATION_PAYMENTS)

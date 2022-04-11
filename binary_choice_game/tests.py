import random
from typing import Callable, Dict, List, Type

from otree.api import Bot, Submission, expect, Page

from binary_choice_game.constants import C
from binary_choice_game.controller.pref_elicit_page import PrefElicitPage
from binary_choice_game.controller.stg3_intro_page import Stg3IntroPage
from binary_choice_game.controller.realized_pref_page import RealizedPrefPage
from binary_choice_game.controller.understanding_testing_4 import UnderstandingTesting4
from binary_choice_game.models import Player, Trial
from binary_choice_game.utils import get_rand_bool
from binary_choice_game.controller import QnPage, StartPage, Stg2IntroPage


def get_mock_input_data(num_trials: int):
    return [
        dict(
            button=random.choice(["L", "R"]),
            start_timestamp_ms=(2 * i) * 500 + (get_rand_bool() * 2 - 1) * 500,
            end_timestamp_ms=(2 * i + 1) * 500 + (get_rand_bool() * 2 - 1) * 500,
        )
        for i in range(num_trials)
    ]


MOCK_INPUT_DATA_BY_STAGE: Dict[int, List[dict]] = {
    stage: get_mock_input_data(num_trials)
    for stage, num_trials in C.NUM_TRIALS_BY_STAGE.items()
}


def call_live_method(
    method: Callable[[Player, dict], dict],
    page_class: Type[Page],
    round_number: int,
    case: str,
    **kwargs
):
    if page_class == QnPage:
        for idx, data_from_client in enumerate(
            [dict()] + MOCK_INPUT_DATA_BY_STAGE[round_number]
        ):
            server_response = method(1, data_from_client)
            assert 1 in server_response
            if idx < C.NUM_TRIALS_BY_STAGE[round_number]:
                assert all(
                    k in server_response[1]
                    for k in ["left_option", "right_option", "rec", "progress"]
                )
            else:
                assert server_response[1].get("is_finished")

    elif page_class == PrefElicitPage:
        for _ in range(C.NUM_PREF_ELICIT_TRIALS):
            if case == "stg3_rec":
                method(1, dict(response=0))
            elif case == "stg3_noRec":
                method(1, dict(response=1))


class PlayerBot(Bot):

    cases = ["stg3_rec", "stg3_noRec"]

    def play_round(self):
        # text for each round is displayed correctly in html
        if self.round_number == 1:
            expect(
                "You have finished the understanding testing questions.",
                "in",
                self.html,
            )
            expect("Now you can start Part 1.", "in", self.html)
        elif self.round_number == 2:
            # participant is assigned a valid treatment
            treatments = self.session.config.get("treatments")
            expect(self.player.participant.treatment, "in", treatments)

            expect("You have finished Part 1.", "in", self.html)
            expect("Please wait for Part 2 to start.", "in", self.html)
        elif self.round_number == 3:
            expect("You have finished Part 2.", "in", self.html)
            expect("Please wait for Part 3 to start.", "in", self.html)
        else:
            raise Exception("There should only be three rounds.")

        yield StartPage
        if self.session.config.get(
            "mode"
        ) == "experiment" and self.participant.treatment in [
            "R_Random",
            "R_Maj",
            "R_CF",
            "R_CBF",
        ]:
            if self.round_number == 2:
                yield Stg2IntroPage
                yield UnderstandingTesting4
            elif self.round_number == 3:
                yield Stg3IntroPage
                yield Submission(PrefElicitPage, check_html=False)
                yield RealizedPrefPage

        yield Submission(QnPage, check_html=False)
        trials = Trial.filter(player=self.player)

        # all questions are shown and recorded
        expected_questions = set(
            C.QUESTIONS_DF_BY_STAGE[self.round_number]["id"].to_list()
        )
        recorded_questions = set([trial.problem_id for trial in trials])
        expect(recorded_questions, expected_questions)

        # all responses and timestamps are recorded correctly
        recorded_input_data = [
            dict(
                button=trial.button,
                start_timestamp_ms=int(trial.start_str_timestamp_ms),
                end_timestamp_ms=int(trial.end_str_timestamp_ms),
            )
            for trial in trials
        ]
        expect(recorded_input_data, MOCK_INPUT_DATA_BY_STAGE[self.round_number])

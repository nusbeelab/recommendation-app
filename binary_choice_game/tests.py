from typing import Callable
from otree.api import Bot, Submission, expect
from binary_choice_game.constants import C
from binary_choice_game.models import Player, Trial
from binary_choice_game.utils import get_rand_bool

from binary_choice_game.views import QnPage, StartPage


mock_input_data = [
    dict(
        response=get_rand_bool(),
        start_timestamp_ms=(2 * i) * 500 + (get_rand_bool() * 2 - 1) * 500,
        end_timestamp_ms=(2 * i + 1) * 500 + (get_rand_bool() * 2 - 1) * 500,
    )
    for i in range(len(C.QUESTIONS))
]

mock_data_from_client = [dict()] + mock_input_data


def call_live_method(method: Callable[[Player, dict], dict], **kwargs):
    for idx, data_from_client in enumerate(mock_data_from_client):
        server_response = method(1, data_from_client)
        assert 1 in server_response
        if idx < len(C.QUESTIONS):
            assert all(
                k in server_response[1] for k in ["optionA", "optionB", "rec"]
            )
        else:
            assert server_response[1].get("is_finished")


class PlayerBot(Bot):
    def play_round(self):
        session_name = self.session.config.get("name")
        if session_name in C.TREATMENTS:
            # player is assigned the recommendation algo as configured
            expect(self.player.treatment, session_name)
            # description of the recommendation algo is displayed in html
            expect(C.REC_ALGO_DESC.get(session_name), "in", self.html)
        else:
            # player is assigned a valid treatment
            expect(self.player.treatment, "in", C.TREATMENTS)
            # description of the recommendation algo is displayed in html
            expect(C.REC_ALGO_DESC.get(self.player.treatment), "in", self.html)
        yield StartPage

        yield Submission(QnPage, check_html=False)
        session_name = self.session.config.get("name")
        trials = Trial.filter(player=self.player)

        # all questions are shown and recorded
        questions = set(frozenset(qn) for qn in C.QUESTIONS)
        recorded_questions = set(
            frozenset((trial.optionA, trial.optionB)) for trial in trials
        )
        expect(recorded_questions, questions)

        # all responses and timestamps are recorded correctly
        recorded_input_data = [
            dict(
                response=trial.response,
                start_timestamp_ms=int(trial.start_str_timestamp_ms),
                end_timestamp_ms=int(trial.end_str_timestamp_ms)
            )
            for trial in trials
        ]
        expect(recorded_input_data, mock_input_data)

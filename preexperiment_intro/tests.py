from typing import Callable, List, Type
from otree.api import Page, Bot, expect, Submission

from preexperiment_intro import (
    C,
    ProlificIdPage,
    QnIntroPage,
    RewardIntroPage,
    UnderstandingTesting1,
    UnderstandingTesting2,
    UnderstandingTesting3,
    WelcomePage,
    WrongAnsPage,
)


QN1_WRONG_ANS = [True, False, False, False]
QN2_WRONG_ANS = [True, False, False, True]
QN3_WRONG_ANS = [False, False, True, True]


def call_live_method(
    method: Callable[[int, List[bool]], None],
    case: str,
    page_class: Type[Page],
    **kwargs
):
    if case == "fail_1":
        if page_class == UnderstandingTesting1:
            method(1, QN1_WRONG_ANS)
        else:
            raise Exception
    elif case == "fail_2":
        if page_class == UnderstandingTesting1:
            method(1, C.QN1_CORRECT_ANS)
        elif page_class == UnderstandingTesting2:
            method(1, QN2_WRONG_ANS)
        else:
            raise Exception
    elif case == "fail_3":
        if page_class == UnderstandingTesting1:
            method(1, C.QN1_CORRECT_ANS)
        elif page_class == UnderstandingTesting2:
            method(1, C.QN2_CORRECT_ANS)
        elif page_class == UnderstandingTesting3:
            method(1, QN3_WRONG_ANS)
        else:
            raise Exception
    elif case == "pass":
        if page_class == UnderstandingTesting1:
            method(1, C.QN1_CORRECT_ANS)
        elif page_class == UnderstandingTesting2:
            method(1, C.QN2_CORRECT_ANS)
        elif page_class == UnderstandingTesting3:
            method(1, C.QN3_CORRECT_ANS)
        else:
            raise Exception


class PlayerBot(Bot):

    cases = ["fail_1", "fail_2", "fail_3", "pass"]

    def play_round(self):
        expect(self.player.pass_testing_qns, True)

        yield ProlificIdPage, dict(prolific_id="test_prolific_id")
        expect(self.player.prolific_id, "test_prolific_id")

        yield WelcomePage
        yield QnIntroPage
        yield RewardIntroPage

        yield UnderstandingTesting1
        if self.case == "fail_1":
            expect(self.player.pass_testing_qns, False)
            expect(
                "Sorry, you answer the understanding test wrongly. You cannot proceed to participate in the experiment.",
                "in",
                self.html,
            )
            yield Submission(WrongAnsPage, check_html=False)
            return

        yield UnderstandingTesting2
        if self.case == "fail_2":
            expect(self.player.pass_testing_qns, False)
            expect(
                "Sorry, you answer the understanding test wrongly. You cannot proceed to participate in the experiment.",
                "in",
                self.html,
            )
            yield Submission(WrongAnsPage, check_html=False)
            return

        yield UnderstandingTesting3
        if self.case == "fail_3":
            expect(self.player.pass_testing_qns, False)
            expect(
                "Sorry, you answer the understanding test wrongly. You cannot proceed to participate in the experiment.",
                "in",
                self.html,
            )
            yield Submission(WrongAnsPage, check_html=False)
            return

        if self.case == "pass":
            expect(self.player.pass_testing_qns, True)
        else:
            raise Exception

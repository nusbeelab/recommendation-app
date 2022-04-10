from typing import Callable, Type
from otree.api import Page, Bot, expect, Submission

from intro import (
    C,
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
    method: Callable[[int, dict], None], case: str, page_class: Type[Page], **kwargs
):
    if case == "fail_qn1":
        if page_class == UnderstandingTesting1:
            method(1, dict(choices=QN1_WRONG_ANS))
            method(1, dict(choices=QN1_WRONG_ANS))
        else:
            raise Exception
    elif case == "fail_qn1_2tries_qn3_fail":
        if page_class == UnderstandingTesting1:
            method(1, dict(choices=QN1_WRONG_ANS))
            method(1, dict(choices=C.UT_ANS[1]))
        elif page_class == UnderstandingTesting2:
            method(1, dict(choices=C.UT_ANS[2]))
        elif page_class == UnderstandingTesting3:
            method(1, dict(choices=QN3_WRONG_ANS))
            method(1, dict(choices=QN3_WRONG_ANS))
        else:
            raise Exception
    elif case == "pass_all_first_tries":
        if page_class == UnderstandingTesting1:
            method(1, dict(choices=C.UT_ANS[1]))
        elif page_class == UnderstandingTesting2:
            method(1, dict(choices=C.UT_ANS[2]))
        elif page_class == UnderstandingTesting3:
            method(1, dict(choices=C.UT_ANS[3]))
        else:
            raise Exception
    elif case == "pass_qn2_2tries":
        if page_class == UnderstandingTesting1:
            method(1, dict(choices=C.UT_ANS[1]))
        elif page_class == UnderstandingTesting2:
            method(1, dict(choices=QN2_WRONG_ANS))
            method(1, dict(choices=C.UT_ANS[2]))
        elif page_class == UnderstandingTesting3:
            method(1, dict(choices=C.UT_ANS[3]))
        else:
            raise Exception
    else:
        raise Exception


class PlayerBot(Bot):

    cases = [
        "fail_qn1",
        "fail_qn1_2tries_qn3_fail",
        "pass_all_first_tries",
        "pass_qn2_2tries",
    ]

    def play_round(self):
        yield WelcomePage
        yield QnIntroPage
        yield RewardIntroPage
        yield UnderstandingTesting1
        if self.case == "fail_qn1":
            expect(self.player.qn_1_status, "fail_2")
            expect(self.player.qn_1_num_tries, 2)
            expect(self.player.qn_2_status, "unanswered")
            expect(self.player.qn_2_num_tries, 0)
            expect(self.player.qn_3_status, "unanswered")
            expect(self.player.qn_3_num_tries, 0)
            expect(
                "Sorry, you answer the understanding test wrongly. You cannot proceed to participate in the experiment.",
                "in",
                self.html,
            )
            yield Submission(WrongAnsPage, check_html=False)
            return

        yield UnderstandingTesting2
        yield UnderstandingTesting3

        if self.case == "fail_qn1_2tries_qn3_fail":
            expect(self.player.qn_1_status, "pass")
            expect(self.player.qn_1_num_tries, 2)
            expect(self.player.qn_2_status, "pass")
            expect(self.player.qn_2_num_tries, 1)
            expect(self.player.qn_3_status, "fail_2")
            expect(self.player.qn_3_num_tries, 2)
            expect(
                "Sorry, you answer the understanding test wrongly. You cannot proceed to participate in the experiment.",
                "in",
                self.html,
            )
            yield Submission(WrongAnsPage, check_html=False)
            return

        if self.case == "pass_all_first_tries":
            expect(self.player.qn_1_status, "pass")
            expect(self.player.qn_1_num_tries, 1)
            expect(self.player.qn_2_status, "pass")
            expect(self.player.qn_2_num_tries, 1)
            expect(self.player.qn_3_status, "pass")
            expect(self.player.qn_3_num_tries, 1)
            return

        if self.case == "pass_qn2_2tries":
            expect(self.player.qn_1_status, "pass")
            expect(self.player.qn_1_num_tries, 1)
            expect(self.player.qn_2_status, "pass")
            expect(self.player.qn_2_num_tries, 2)
            expect(self.player.qn_3_status, "pass")
            expect(self.player.qn_3_num_tries, 1)
            return

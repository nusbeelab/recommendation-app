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


class PlayerBot(Bot):
    def play_round(self):
        yield ProlificIdPage, dict(prolific_id="test_prolific_id")
        yield WelcomePage
        yield QnIntroPage
        yield RewardIntroPage
        yield UnderstandingTesting1
        yield UnderstandingTesting2
        yield UnderstandingTesting3

        expect(self.player.prolific_id, "test_prolific_id")

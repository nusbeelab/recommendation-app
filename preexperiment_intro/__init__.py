from typing import Literal, Optional
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page


class C(BaseConstants):
    NAME_IN_URL = "intro"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


QN_STATUSES = ["unanswered", "fail_1", "fail_2", "pass"]


class Player(BasePlayer):
    prolific_id = models.StringField()
    qn_1_status = models.StringField(choices=QN_STATUSES, initial=QN_STATUSES[0])
    qn_2_status = models.StringField(choices=QN_STATUSES, initial=QN_STATUSES[0])
    qn_3_status = models.StringField(choices=QN_STATUSES, initial=QN_STATUSES[0])


def is_player_not_failing(player: Player):
    return all(
        getattr(player, f"qn_{qn_num}_status") != "fail_2" for qn_num in [1, 2, 3]
    )


class CustomPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return is_player_not_failing(player)


class ProlificIdPage(CustomPage):
    form_model = "player"
    form_fields = ["prolific_id"]


class WelcomePage(CustomPage):
    pass


class QnIntroPage(CustomPage):
    pass


class RewardIntroPage(CustomPage):
    pass


def get_live_method(qn_num: Literal[1, 2, 3]):
    def live_method(player: Player, qn_status: str):
        qn_status_attr = f"qn_{qn_num}_status"
        setattr(player, qn_status_attr, qn_status)

    return live_method


def get_js_vars(qn_num: Literal[1, 2, 3]):
    def js_vars(player: Player):
        return dict(qn_status=getattr(player, f"qn_{qn_num}_status"))

    return js_vars


class UnderstandingTesting1(CustomPage):
    live_method = get_live_method(1)
    js_vars = get_js_vars(1)


class UnderstandingTesting2(CustomPage):
    live_method = get_live_method(2)
    js_vars = get_js_vars(2)


class UnderstandingTesting3(CustomPage):
    live_method = get_live_method(3)
    js_vars = get_js_vars(3)


class WrongAnsPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not is_player_not_failing(player)

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        try:
            return upcoming_apps[-1]
        except:
            return None


page_sequence = [
    ProlificIdPage,
    WelcomePage,
    QnIntroPage,
    RewardIntroPage,
    UnderstandingTesting1,
    UnderstandingTesting2,
    UnderstandingTesting3,
    WrongAnsPage,
]

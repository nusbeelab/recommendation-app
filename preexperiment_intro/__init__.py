import logging
from typing import Literal
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page

logging.config.fileConfig("logging.conf")


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
    qn_1_status = models.StringField(choices=QN_STATUSES, initial=QN_STATUSES[0])
    qn_1_num_tries = models.IntegerField(initial=0)
    qn_2_status = models.StringField(choices=QN_STATUSES, initial=QN_STATUSES[0])
    qn_2_num_tries = models.IntegerField(initial=0)
    qn_3_status = models.StringField(choices=QN_STATUSES, initial=QN_STATUSES[0])
    qn_3_num_tries = models.IntegerField(initial=0)


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


def get_qn_num_tries(old_qn_status):
    if old_qn_status == "unanswered":
        return 1
    if old_qn_status == "fail_1":
        return 2
    return None


def get_live_method(qn_num: Literal[1, 2, 3]):
    def live_method(player: Player, data: dict):
        logger = logging.getLogger(__name__)

        qn_status_attr = f"qn_{qn_num}_status"
        qn_num_tries_attr = f"qn_{qn_num}_num_tries"
        old_qn_status = getattr(player, qn_status_attr)
        qn_num_tries = get_qn_num_tries(old_qn_status)

        logger.info(
            f"Participant {player.participant.code}, understanding testing question {qn_num}, number of tries: {qn_num_tries}, data received from client: {data}."
        )

        setattr(player, qn_status_attr, data.get("status"))
        setattr(player, qn_num_tries_attr, qn_num_tries)

    return live_method


def get_js_vars(qn_num: Literal[1, 2, 3]):
    def js_vars(player: Player):
        logger = logging.getLogger(__name__)

        qn_status = getattr(player, f"qn_{qn_num}_status")
        logger.info(
            f"Participant {player.participant.code}, understanding testing question {qn_num}, question status sent to client: {qn_status}."
        )
        return dict(qn_status=qn_status)

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
    # ProlificIdPage,
    WelcomePage,
    QnIntroPage,
    RewardIntroPage,
    UnderstandingTesting1,
    UnderstandingTesting2,
    UnderstandingTesting3,
    WrongAnsPage,
]

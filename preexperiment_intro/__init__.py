from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models

from common import CustomPage, set_qualified_participant_if_none


class C(BaseConstants):
    NAME_IN_URL = "intro"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    mturk_id = models.StringField()


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        set_qualified_participant_if_none(player)


class MTurkIdPage(CustomPage):
    form_model = "player"
    form_fields = ["mturk_id"]


class WelcomePage(CustomPage):
    pass


class QnIntroPage(CustomPage):
    pass


class RewardIntroPage(CustomPage):
    pass


class UnderstandingTesting(CustomPage):
    @staticmethod
    def live_method(player: Player, _):
        player.participant.is_qualified = False


class UnderstandingTesting1(UnderstandingTesting):
    pass


class UnderstandingTesting2(UnderstandingTesting):
    pass


class UnderstandingTesting3(UnderstandingTesting):
    pass


page_sequence = [
    MTurkIdPage,
    WelcomePage,
    QnIntroPage,
    RewardIntroPage,
    UnderstandingTesting1,
    UnderstandingTesting2,
    UnderstandingTesting3,
]

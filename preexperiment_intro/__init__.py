from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page


class C(BaseConstants):
    NAME_IN_URL = "intro"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    QN1_CORRECT_ANS = [True, False, False, True]
    QN2_CORRECT_ANS = [False, True, True, False]
    QN3_CORRECT_ANS = [False, True, False, True]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass_testing_qns = models.BooleanField(initial=True)
    prolific_id = models.StringField()


class CustomPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.pass_testing_qns


class ProlificIdPage(CustomPage):
    form_model = "player"
    form_fields = ["prolific_id"]


class WelcomePage(CustomPage):
    pass


class QnIntroPage(CustomPage):
    pass


class RewardIntroPage(CustomPage):
    pass


class UnderstandingTesting1(CustomPage):
    def live_method(player: Player, data):
        player.pass_testing_qns = data == C.QN1_CORRECT_ANS


class UnderstandingTesting2(CustomPage):
    def live_method(player: Player, data):
        player.pass_testing_qns = data == C.QN2_CORRECT_ANS


class UnderstandingTesting3(CustomPage):
    def live_method(player: Player, data):
        player.pass_testing_qns = data == C.QN3_CORRECT_ANS


class WrongAnsPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.pass_testing_qns


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

from otree.api import BasePlayer, Page


class CustomPage(Page):
    @staticmethod
    def is_displayed(player: BasePlayer):
        return player.participant.is_qualified


def set_qualified_participant_if_none(player: BasePlayer):
    participant = player.participant
    if "is_qualified" not in participant.vars or participant.is_qualified == None:
        participant.is_qualified = True

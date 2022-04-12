import logging
import random
from typing import Literal
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page

logging.config.fileConfig("logging.conf")


class C(BaseConstants):
    NAME_IN_URL = "hypothetical_qns"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    qns = ["1", "2"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            round_numbers = list(range(1, C.NUM_ROUNDS + 1))
            random.shuffle(round_numbers)
            p.participant.qn_rounds = dict(zip(C.qns, round_numbers))


class Player(BasePlayer):
    qn1_response = models.BooleanField()
    qn2_response = models.BooleanField()


class Qn1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == player.participant.qn_rounds["1"]

    @staticmethod
    def live_method(player: Player, data: dict):
        logger = logging.getLogger(__name__)
        logger.info(f"Received data from player {player.participant.code}: {data}.")
        try:
            player.qn1_response = data.get("response")
            return {player.id_in_group: True}
        except Exception as err:
            logger.error(err)
            raise err


class Qn2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == player.participant.qn_rounds["2"]

    @staticmethod
    def live_method(player: Player, data: dict):
        logger = logging.getLogger(__name__)
        logger.info(f"Received data from player {player.participant.code}: {data}.")
        try:
            player.qn2_response = data.get("response")
            return {player.id_in_group: True}
        except Exception as err:
            logger.error(err)
            raise err


page_sequence = [Qn1, Qn2]

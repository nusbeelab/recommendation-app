import logging
from typing import Iterable
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Page


class C(BaseConstants):
    NAME_IN_URL = "end"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


def custom_export(players: Iterable[Player]):
    logger = logging.getLogger(__name__)

    logger.info("Exporting data.")

    # header row
    yield ["session_code", "participant_code", "treatment"]
    try:
        for p in players:
            yield [p.session.code, p.participant.code, p.participant.treatment]
    except Exception as err:
        logger.error(err)


page_sequence = []

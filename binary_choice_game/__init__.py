import logging.config
from binary_choice_game.constants import C
from binary_choice_game.models import (
    Subsession,
    Group,
    Player,
    Trial,
)
from binary_choice_game.functions import creating_session, custom_export
from binary_choice_game.controller import page_sequence

logging.config.fileConfig("logging.conf")

doc = """
Binary choice questions
"""

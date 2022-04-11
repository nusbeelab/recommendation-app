from binary_choice_game.models import Player


def is_assigned_rec_treatment(player: Player):
    return player.participant.treatment in [
        "R_Random",
        "R_Maj",
        "R_CF",
        "R_CBF",
    ]

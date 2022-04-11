from binary_choice_game.controller.pref_elicit_page import PrefElicitPage
from binary_choice_game.controller.start_page import StartPage
from binary_choice_game.controller.stg2_intro_page import Stg2IntroPage
from binary_choice_game.controller.qn_page import QnPage
from binary_choice_game.controller.end_page import EndPage
from binary_choice_game.controller.stg3_intro1_page import Stg3Intro1Page
from binary_choice_game.controller.understanding_testing_4 import UnderstandingTesting4


page_sequence = [
    StartPage,
    Stg2IntroPage,
    UnderstandingTesting4,
    # Stg3Intro1Page,
    # PrefElicitPage,
    QnPage,
    EndPage,
]

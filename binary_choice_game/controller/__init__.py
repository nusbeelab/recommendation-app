from binary_choice_game.controller.pref_elicit_page import PrefElicitPage
from binary_choice_game.controller.start_page import StartPage
from binary_choice_game.controller.stg2_intro_page import Stg2IntroPage
from binary_choice_game.controller.qn_page import QnPage
from binary_choice_game.controller.end_page import EndPage
from binary_choice_game.controller.stg3_intro_page1 import Stg3IntroPage1
from binary_choice_game.controller.realized_pref_page import RealizedPrefPage
from binary_choice_game.controller.stg3_intro_page2 import Stg3IntroPage2
from binary_choice_game.controller.understanding_testing_4 import UnderstandingTesting4


page_sequence = [
    StartPage,
    Stg2IntroPage,
    UnderstandingTesting4,
    Stg3IntroPage1,
    Stg3IntroPage2,
    PrefElicitPage,
    RealizedPrefPage,
    QnPage,
    EndPage,
]

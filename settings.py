from os import environ

QUESTIONS_CSV_FILE = "parameters_20Mar2022.csv"

SESSION_CONFIGS = [
    dict(
        name="experiment",
        display_name="Experiment",
        app_sequence=[
            "preexperiment_intro",
            "binary_choice_game",
            "questionnaire",
            "empty_app",
        ],
        num_demo_participants=1,
        treatments=["NoR", "R_Random", "R_CF", "R_CBF"],
    ),
    dict(
        name="game_NoR",
        display_name="Problems, NoR",
        app_sequence=["binary_choice_game"],
        num_demo_participants=1,
        treatments=["NoR"],
    ),
    dict(
        name="game_R_Random",
        display_name="Problems, R_Random",
        app_sequence=["binary_choice_game"],
        num_demo_participants=1,
        treatments=["R_Random"],
    ),
    dict(
        name="game_R_Maj",
        display_name="Problems, R_Maj",
        app_sequence=["binary_choice_game"],
        num_demo_participants=1,
        treatments=["R_Maj"],
    ),
    # dict(
    #     name="game_R_CF",
    #     display_name="Problems, R_CF",
    #     app_sequence=["binary_choice_game"],
    #     num_demo_participants=1,
    #     treatments=["R_CF"],
    # ),
    dict(
        name="game_R_CBF",
        display_name="Problems, R_CBF",
        app_sequence=["binary_choice_game"],
        num_demo_participants=1,
        treatments=["R_CBF"],
    ),
    dict(
        name="preexperiment",
        display_name="Pre-experiment",
        app_sequence=[
            "preexperiment_intro",
            "binary_choice_game",
            "questionnaire",
            "empty_app",
        ],
        num_demo_participants=1,
        treatments=["NoR"],
    ),
    dict(
        name="preexperiment_intro",
        display_name="Pre-experiment Intro",
        app_sequence=["preexperiment_intro"],
        num_demo_participants=1,
    ),
    dict(
        name="preexperiment_game",
        display_name="Pre-experiment Problems",
        app_sequence=["binary_choice_game"],
        num_demo_participants=1,
        treatments=["NoR"],
    ),
    dict(
        name="preexperiment_questionnaire",
        display_name="Pre-experiment Questionnaire",
        app_sequence=["questionnaire"],
        num_demo_participants=1,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ["finished", "treatment"]
SESSION_FIELDS = ["prolific_completion_url"]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = True

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = "7302347950116"

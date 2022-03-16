from os import environ

COMMON_CONFIGS = dict(
    num_demo_participants=1,
    app_sequence=["binary_choice_game"],
    question_params_file="parameters_13Mar2022.csv",
)

SESSION_CONFIGS = [
    dict(name="NoR", display_name="Pre-experiment", **COMMON_CONFIGS),
    # dict(
    #     name="R",
    #     display_name="Randomized Treatments",
    #     **COMMON_CONFIGS
    # ),
    # dict(name="NoR", display_name="No Recommendations", **COMMON_CONFIGS),
    # dict(
    #     name="R_Random",
    #     display_name="Random Recommendations",
    #     **COMMON_CONFIGS
    # ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

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

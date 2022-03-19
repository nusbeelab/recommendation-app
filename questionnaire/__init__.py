from otree.api import (
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    models,
    widgets,
    Page,
)

GENDER_CHOICES = [[False, "Male"], [True, "Female"]]
AGE_CHOICES = [
    "<=18 years old",
    "18-24 years old",
    "25-34 years old",
    "35-44 years old",
    "45-54 years old",
    "55-64 years old",
    ">=65 years old",
]
EDUCATION_LEVEL_CHOICES = [
    "High School",
    "Some College",
    "Associates",
    "Bachelor's",
    "Advanced",
]
EMPLOYMENT_STATUS_CHOICES = [
    "Employed full time (40 or more hours per week)",
    "Employed part time (up to 39 hours per week)",
    "Unemployed and currently looking for work",
    "Unemployed and not currently looking for work",
    "Student",
    "Retired",
    "Homemaker",
    "Self-employed",
    "Unable to work",
]
MARTIAL_STATUS_CHOICES = [
    "Married",
    "Living together as married",
    "Divorced",
    "Separated",
    "Widowed",
    "Single",
]
CHILDREN_NUM_CHOICES = [
    "No children",
    "One child",
    "Two children",
    "Three children",
    "More than three children",
]
CHILD_SEX_CHOICES = ["Boy", "Girl"]
CHILDREN_SEX_CHOICES = [
    "No boys",
    "One boy",
    "Two boys",
    "Three boys",
    "More than three boys",
]
AI_AWARENESS_CHOICES = [
    "Not at all aware",
    "Slightly aware",
    "Somewhat aware",
    "Moderately aware",
    "Extremely aware",
]
AI_OPINION_CHOICES = [
    "Extremely harmful",
    "Slightly harmful",
    "Neutral",
    "Slight helpful",
    "Extremely helpful",
]


class C(BaseConstants):
    NAME_IN_URL = "questionnaire"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.BooleanField(choices=GENDER_CHOICES, widget=widgets.RadioSelect)
    age = models.StringField(choices=AGE_CHOICES, widget=widgets.RadioSelect)
    race = models.StringField()
    nationality = models.StringField()
    education_level = models.StringField(
        choices=EDUCATION_LEVEL_CHOICES, widget=widgets.RadioSelect
    )
    employment_status = models.StringField(
        choices=EMPLOYMENT_STATUS_CHOICES, widget=widgets.RadioSelect
    )
    marital_status = models.StringField(
        choices=MARTIAL_STATUS_CHOICES, widget=widgets.RadioSelect
    )
    children_num = models.StringField(
        choices=CHILDREN_NUM_CHOICES, widget=widgets.RadioSelect
    )
    child_sex = models.StringField(
        choices=CHILD_SEX_CHOICES, widget=widgets.RadioSelect
    )
    children_sex = models.StringField(
        choices=CHILDREN_SEX_CHOICES, widget=widgets.RadioSelect
    )
    religion = models.StringField()
    ai_awareness = models.StringField(
        choices=AI_AWARENESS_CHOICES, widget=widgets.RadioSelect
    )
    ai_opinion = models.StringField(
        choices=AI_OPINION_CHOICES, widget=widgets.RadioSelect
    )


class Gender(Page):
    form_model = "player"
    form_fields = ["gender"]


class Age(Page):
    form_model = "player"
    form_fields = ["age"]


class Race(Page):
    @staticmethod
    def live_method(player: Player, race: str):
        player.race = race
        print(player.race)


class Nationality(Page):
    @staticmethod
    def live_method(player: Player, nationality: str):
        player.nationality = nationality
        print(player.nationality)


class EducationLevel(Page):
    form_model = "player"
    form_fields = ["education_level"]


class EmploymentStatus(Page):
    form_model = "player"
    form_fields = ["employment_status"]


class MaritalStatus(Page):
    form_model = "player"
    form_fields = ["marital_status"]


class ChildrenNum(Page):
    form_model = "player"
    form_fields = ["children_num"]


class ChildSex(Page):
    form_model = "player"
    form_fields = ["child_sex"]

    @staticmethod
    def is_displayed(player: Player):
        return player.children_num == CHILDREN_NUM_CHOICES[1]


class ChildrenSex(Page):
    form_model = "player"
    form_fields = ["children_sex"]

    @staticmethod
    def is_displayed(player: Player):
        return player.children_num in [
            CHILDREN_NUM_CHOICES[i] for i in range(2, len(CHILDREN_NUM_CHOICES))
        ]


class Religion(Page):
    @staticmethod
    def live_method(player: Player, religion: str):
        player.religion = religion
        print(player.religion)


class AiAwareness(Page):
    form_model = "player"
    form_fields = ["ai_awareness"]


class AiOpinion(Page):
    form_model = "player"
    form_fields = ["ai_opinion"]


class Finish(Page):
    @staticmethod
    def before_next_page(player: Player, _):
        player.participant.finished = True


page_sequence = [
    Gender,
    Age,
    Race,
    Nationality,
    EducationLevel,
    EmploymentStatus,
    MaritalStatus,
    ChildrenNum,
    ChildSex,
    ChildrenSex,
    Religion,
    AiAwareness,
    AiOpinion,
    Finish,
]

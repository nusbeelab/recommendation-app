from otree.api import Bot, Submission

from questionnaire import (
    AGE_CHOICES,
    AI_AWARENESS_CHOICES,
    CHILDREN_NUM_CHOICES,
    # CHILD_SEX_CHOICES,
    # CHILDREN_SEX_CHOICES,
    EDUCATION_LEVEL_CHOICES,
    EMPLOYMENT_STATUS_CHOICES,
    GENDER_CHOICES,
    MARTIAL_STATUS_CHOICES,
    OPINION_CHOICES,
    Age,
    AiAwareness,
    AiOpinion,
    ArticleRecOpinion,
    ChildrenNum,
    # ChildSex,
    # ChildrenSex,
    EducationLevel,
    EmploymentStatus,
    Finish,
    Gender,
    MaritalStatus,
    Nationality,
    ProdRecOpinion,
    Race,
    Religion,
)


class PlayerBot(Bot):
    def play_round(self):
        yield Gender, dict(gender=GENDER_CHOICES[0])
        yield Age, dict(age=AGE_CHOICES[0])
        yield Submission(Race, dict(race="Asian"), check_html=False)
        yield Submission(Nationality, dict(nationality="American"), check_html=False)
        yield EducationLevel, dict(education_level=EDUCATION_LEVEL_CHOICES[0])
        yield EmploymentStatus, dict(employment_status=EMPLOYMENT_STATUS_CHOICES[0])
        yield MaritalStatus, dict(marital_status=MARTIAL_STATUS_CHOICES[0])
        yield ChildrenNum, dict(children_num=CHILDREN_NUM_CHOICES[0])
        # yield ChildSex, dict(child_sex=CHILD_SEX_CHOICES[0])
        # yield ChildrenSex, dict(children_sex=CHILDREN_SEX_CHOICES[0])
        yield Submission(Religion, dict(religion="Buddhism"), check_html=False)
        yield AiAwareness, dict(ai_awareness=AI_AWARENESS_CHOICES[0])
        yield AiOpinion, dict(ai_opinion=OPINION_CHOICES[0])
        if self.session.config.get("mode") == "experiment":
            yield ProdRecOpinion, dict(prod_rec_opinion=OPINION_CHOICES[0])
            yield ArticleRecOpinion, dict(article_rec_opinion=OPINION_CHOICES[0])
        yield Submission(Finish, check_html=False)

from binary_choice_game.models import Player, Trial
from binary_choice_game.functions import live_method
from otree.api import Page
from otree.common import get_app_label_from_import_path


class CustomPage(Page):
    def get_template_name(self):
        if self.template_name is not None:
            return self.template_name
        return "{}/views/{}.html".format(
            get_app_label_from_import_path(self.__module__),
            self.__class__.__name__,
        )


class QnPage(CustomPage):
    live_method = live_method


class Results(CustomPage):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(trials=Trial.filter(player=player))


page_sequence = [QnPage, Results]

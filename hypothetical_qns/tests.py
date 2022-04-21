from otree.api import Bot, Submission

from hypothetical_qns import Qn1, Qn2


class PlayerBot(Bot):
    def play_round(self):
        if self.session.config.get("mode") == "experiment":
            if self.participant.qn_rounds[self.round_number] == 1:
                yield Submission(Qn1, check_html=False)
            elif self.participant.qn_rounds[self.round_number] == 2:
                yield Submission(Qn2, check_html=False)

import unittest

from binary_choice_game.recommendations import (
    NoneRecommender,
    RandomRecommender,
    get_recommender,
)


class TestRecommendations(unittest.TestCase):
    def test_NoneRecommender(self):
        self.assertIsNone(NoneRecommender().rec(None, None))

    def test_getRecommender_success_recommenderFound(self):
        self.assertIsInstance(get_recommender("R_Random"), RandomRecommender)

    def test_getRecommender_failure_invalidTreatment(self):
        self.assertRaises(ValueError, lambda: get_recommender("invalid"))


if __name__ == "__main__":
    unittest.main()

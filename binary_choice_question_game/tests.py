from datetime import datetime
import unittest

from binary_choice_question_game.utils import timestamp2datetime, try_else_none


class TestMain(unittest.TestCase):
    pass


class TestUtils(unittest.TestCase):
    def test_readQns_success(self):
        pass

    def test_readQns_failure(self):
        pass

    def test_tryElseNone_success(self):
        self.assertEqual(try_else_none(lambda: True), True)

    def test_tryElseNone_failure(self):
        self.assertIsNone(
            try_else_none(lambda: (_ for _ in ()).throw(Exception()))
        )

    def test_timestamp2datetime_success(self):
        self.assertEqual(
            timestamp2datetime(1645345997672), datetime(2022, 2, 20, 15, 33, 18)
        )

    def test_timestamp2datetime_failure(self):
        self.assertIsNone(timestamp2datetime(None))


if __name__ == "__main__":
    unittest.main()

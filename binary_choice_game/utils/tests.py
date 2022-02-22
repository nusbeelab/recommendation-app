from datetime import datetime
import unittest

from binary_choice_game.utils import (
    timestamp2utcdatetime,
    try_else_none,
)


class TestUtils(unittest.TestCase):
    def test_tryElseNone_success(self):
        self.assertEqual(try_else_none(lambda: True), True)

    def test_tryElseNone_failure(self):
        self.assertIsNone(
            try_else_none(lambda: (_ for _ in ()).throw(Exception()))
        )

    def test_timestamp2datetime_success(self):
        self.assertEqual(
            timestamp2utcdatetime(1645345997672),
            datetime(2022, 2, 20, 8, 33, 18),
        )

    def test_timestamp2datetime_failure(self):
        self.assertIsNone(timestamp2utcdatetime(None))


if __name__ == "__main__":
    unittest.main()

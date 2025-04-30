import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from app.logger import get_logger
from app.logger.database import get_recent_log
from app.utils.time import get_current_time_str
from app.utils.random import generate_random_string

class TestLogger(unittest.TestCase):
    def test_logger(self):
        logger = get_logger()

        test_message = f"logger test, {get_current_time_str()}, {generate_random_string(24)}"
        logger.info(test_message)

        log = get_recent_log(test_message)

        self.assertIsNotNone(log)
        self.assertEqual(log["message"], test_message)

if __name__ == "__main__":
    unittest.main()
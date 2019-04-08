import unittest
import py.utilities as utils
from py.logger import Logger

class LoggerTestCase(unittest.TestCase):

    def setUp(self):
        self.logger = Logger(0, "Test", "H4")

    def testInit(self):
        self.assertEqual(self.logger.info, "INFO")

    def testWriteInfo(self):
        self.logger.log_info("TestComponent", "TetMessage")


if __name__ == '__main__':
    unittest.main()
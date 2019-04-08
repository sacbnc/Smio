import unittest
import py.api as api
from py.logger import Logger
from py.stream import Stream

class StreamTestCase(unittest.TestCase):

    def testGetCandle(self):
        logger = Logger(0, "EUR_USD", 30)
        stream = Stream(logger)
        candle = stream.get_candle()

        self.assertIsNotNone(candle)
        self.assertIsNotNone(candle.open)

    def testGetCandles(self):
        logger = Logger(0, "EUR_USD", 30)
        stream = Stream(logger)
        candles = stream.get_candles(10)
        self.assertEqual(len(candles), 10)



if __name__ == '__main__':
    unittest.main()
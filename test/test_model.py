import unittest
import datetime
from py.logger import Logger
from py.candle import Candle
from py.model import Model


class ModelTestCase(unittest.TestCase):

    def getUpModel(self):
        return self.getModel(1)

    def getDownModel(self):
        return self.getModel(-1)

    def getModel(self, dir=1):
        atr_len = 14
        ma_len = 20

        now = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z"))
        candles = [Candle(now, 20000, 20000, 20000+dir, 20000+dir, 10)]

        while len(candles) < max(atr_len, ma_len) + 1:
            candles.append(Candle(now,
                           candles[-1].open + (5*dir),
                           candles[-1].high + (5*dir),
                           candles[-1].low + (5*dir),
                           candles[-1].close + (5*dir),
                           candles[-1].volume))

        logger = Logger(0, "TST_SYM", 30)
        return Model(0, 0, logger, candles, atr_len, ma_len)

    def testModelInit(self):
        self.model = self.getUpModel()
        self.assertEqual(self.model.state.position, self.model.candles[-1].close)
        self.assertEqual(self.model.state.sequence, 2)

    def testModelUpCandlesUpdate(self):
        self.model = self.getUpModel()
        candle = Candle(str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z")),
                        self.model.candles[-1].open + 5,
                        self.model.candles[-1].high + 5,
                        self.model.candles[-1].low + 5,
                        self.model.candles[-1].close + 5,
                        self.model.candles[-1].volume)

        self.sequence = self.model.state.sequence
        self.model.input(candle)

        self.assertEqual(self.model.state.sequence, self.sequence+1)
        self.assertEqual(self.model.state.position, candle.close)

    def testModelUpCandlesUpdateNoChange(self):
        self.model = self.getUpModel()
        candle = Candle(str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z")),
                        self.model.candles[-1].open + 2,
                        self.model.candles[-1].high + 2,
                        self.model.candles[-1].low + 2,
                        self.model.candles[-1].close + 2,
                        self.model.candles[-1].volume)

        self.sequence = self.model.state.sequence
        self.model.input(candle)

        self.assertEqual(self.model.state.sequence, self.sequence)
        self.assertNotEqual(self.model.state.position, candle.close)

    def testModelDownCandlesUpdate(self):
        self.model = self.getDownModel()
        candle = Candle(str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z")),
                        self.model.candles[-1].open - 5,
                        self.model.candles[-1].high - 5,
                        self.model.candles[-1].low - 5,
                        self.model.candles[-1].close - 5,
                        self.model.candles[-1].volume)

        self.sequence = self.model.state.sequence
        self.model.input(candle)

        self.assertEqual(self.model.state.sequence, self.sequence-1)
        self.assertEqual(self.model.state.position, candle.close)






if __name__ == '__main__':
    unittest.main()
import unittest
import datetime
from py.logger import Logger
from py.candle import Candle
from py.state import State
from py.intelligence import Intelligence



class IntelligenceTestCase(unittest.TestCase):

    def setUp(self):
        now = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z"))

        candle = Candle(now, 200, 200, 100, 150, 100)
        self.state = State(candle, 5, 100)

        self.distance = 1
        self.tp = 2
        self.sl = 2
        self.trl = 2
        self.min_seq = 3
        self.use_mac = True

        logger = Logger(0, "TST_SYM", 30)
        self.intelligence = Intelligence(0,
                                         0,
                                         logger,
                                         self.distance,
                                         self.tp,
                                         self.sl,
                                         self.trl,
                                         self.min_seq,
                                         self.use_mac)

    def testBuyOrders(self):
        # no order for sequence of 1
        order = self.intelligence.input(self.state)
        self.assertIsNone(order)

        # order for sequence of 3 and above ma
        self.state.sequence = 3
        self.state.ma = self.state.position - 1
        order = self.intelligence.input(self.state)

        self.assertIsNotNone(order)
        self.assertEqual(order.direction, 1)
        self.assertEqual(order.open, self.state.level(self.distance))
        self.assertEqual(order.tp, self.state.level(self.distance + self.tp))
        self.assertEqual(order.sl, self.state.level(self.distance - self.sl))
        self.assertEqual(order.trl, order.open - order.sl)

        # no order for sequence of 3 and below ma
        self.state.ma = self.state.position + 1
        order = self.intelligence.input(self.state)
        self.assertIsNone(order)

        # no take profit
        self.intelligence.tp = 0
        self.state.ma = self.state.position - 1
        order = self.intelligence.input(self.state)
        self.assertIsNotNone(order)


    def testSellOrders(self):
        # order for sequence of -3 and below ma
        self.state.sequence = -3
        self.state.ma = self.state.position + 1
        order = self.intelligence.input(self.state)

        self.assertIsNotNone(order)
        self.assertEqual(order.direction, -1)
        self.assertEqual(order.tp, self.state.level(-self.distance - self.tp))
        self.assertEqual(order.sl, self.state.level(-self.distance + self.sl))
        self.assertEqual(order.trl, order.sl - order.open)

        # No order for sequence of -3 and above ma
        self.state.ma = self.state.position - 1
        order = self.intelligence.input(self.state)
        self.assertIsNone(order)


if __name__ == '__main__':
    unittest.main()
import unittest
from py.logger import Logger
from py.order import Order
from py.broker import Broker

class BrokerTestCase(unittest.TestCase):

    def testPlaceOrder(self):
        logger = Logger(0, "EUR_USD", 30)
        broker = Broker(0, logger, 0.025, '101-004-4759925-003')
        order = Order("Unit test", 1, 1.0020, 0, 1, 1)
        self.assertTrue(broker.input(order))

    def testPlaceOrderNoTP(self):
        logger = Logger(0, "EUR_USD", 30)
        broker = Broker(0, logger, 0.025, '101-004-4759925-003')
        order = Order("Unit test", 1, 1.0020, 0, 1.0000, 1.0000)
        self.assertTrue(broker.input(order))

    def testPlaceOrderNoTPSL(self):
        logger = Logger(0, "EUR_USD", 30)
        broker = Broker(0, logger, 0.025, '101-004-4759925-003')
        order = Order("Unit test", 1, 1.0020, 0, 0, 1.0000)
        self.assertTrue(broker.input(order))

    def testPlaceOrderNoTPSL(self):
        logger = Logger(0, "EUR_USD", 30)
        broker = Broker(0, logger, 0.025, '101-004-4759925-003')
        order = Order("Unit test", 1, 1.0020, 0, 0, 1.0000)
        self.assertTrue(broker.input(order))

    def testPlaceNoOpenOrder(self):
        logger = Logger(0, "EUR_USD", 30)
        broker = Broker(0, logger, 0.025, '101-004-4759925-003')
        order = Order("Unit test", None, None, None, None, None)
        self.assertFalse(broker.input(order))


if __name__ == '__main__':
    unittest.main()
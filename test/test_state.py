import unittest
import datetime
from py.state import State
from py.candle import Candle

class StateTestCase(unittest.TestCase):

    def testStateInit(self):
        now = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z"))
        candle = Candle(now, 15, 20, 10, 20, 10)
        state = State(candle, 5, 100)

        self.assertEqual(state.position, candle.close)


    def testStateUpSequenceUpdateContinuation(self):
        now = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z"))

        candle = Candle(now, 150, 200, 100, 200, 100)
        state = State(candle, 5, 100)

        candle.close += 5
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 2)

        candle.close = state.position + 11
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 4)

        candle.close = state.position + 4
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 4)

        candle.close = state.position + 9
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 5)

        candle.close = state.position + 17
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 8)

        candle = Candle(now, 150, 200, 100, 200, 100)
        state = State(candle, 5, 100)

        candle.close = state.position + 100
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 21)

    def testStateUpSequenceUpdateReversal(self):
        now = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z"))

        candle = Candle(now, 150, 200, 100, 200, 100)
        state = State(candle, 5, 100)

        candle.close -= 5
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 1)

        candle.close = state.position - 9
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 1)

        candle.close = state.position - 11
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, -1)

        candle = Candle(now, 150, 200, 100, 200, 100)
        state = State(candle, 5, 100)

        candle.close = state.position - 100
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, -19)

    def testStateDownSequenceUpdateContinuation(self):
        now = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z"))

        candle = Candle(now, 200, 200, 100, 150, 100)
        state = State(candle, 5, 100)

        candle.close -= 5
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, -2)

        candle.close = state.position - 11
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, -4)

        candle.close = state.position - 4
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, -4)

        candle.close = state.position - 9
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, -5)

        candle.close = state.position - 17
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, -8)

    def testStateDownSequenceUpdateReversals(self):
        now = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000000Z"))

        candle = Candle(now, 200, 200, 100, 150, 100)
        state = State(candle, 5, 100)

        candle.close += 5
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, -1)

        candle.close = state.position + 9
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, -1)

        candle.close = state.position + 11
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 1)

        candle = Candle(now, 200, 200, 100, 150, 100)
        state = State(candle, 5, 100)

        candle.close = state.position + 100
        state.update(candle, 5, 100)
        self.assertEqual(state.sequence, 19)

if __name__ == '__main__':
    unittest.main()
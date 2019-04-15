from py.utilities import normal_round as round

class State:
    @property
    def up(self):
        return self.sequence > 0

    @property
    def down(self):
        return self.sequence < 0

    @property
    def next_brick(self):
        if self.up:
            return self.level(self.continuation)
        elif self.down:
            return self.level(-self.continuation)
        return None

    @property
    def close_brick(self):
        if self.up:
            return self.level(-self.reversal)
        elif self.down:
            return self.level(self.reversal)
        return None

    @property
    def mac(self):
        """
        moving average composition.
        where does price sit relative to the ma
        given its direction?
         up seq & above ma => 1
         down seq & below ma => 1
         up seq and below ma => -1
         down seq and above ma => -1
        """
        if self.up and self.position > self.ma:
            return True
        elif self.down and self.position < self.ma:
            return True
        return False

    def level(self, i):
        return self.position + (self.interval * i)

    def update(self, candle, atr, ma):

        change = candle.close - self.position

        # re-calculate interval and ma
        # this means that new brick sizes
        # will reflect the current atr
        self.interval = atr
        self.ma = ma

        # get either 1 or -1
        direction = 1 if change > 0 else -1

        # calculate how many intervals have been traversed
        # round up or down depending on value of direction
        # to always return the last interval
        distance = round(change / self.interval - (0.5 * direction))

        # if up or down sequence continues
        if (self.up and distance >= self.continuation) or (self.down and distance <= -self.continuation):
            self.position = self.level(distance)
            self.sequence += distance
        # if up or down sequence reverses
        elif (self.up and distance <= -self.reversal) or (self.down and distance >= self.reversal):
            self.position = self.level(distance)
            self.sequence = distance - direction
        else:
            return False

        return True

    def __init__(self, candle, atr, ma, continuation=1, reversal=2):
        self.continuation = continuation
        self.reversal = reversal
        self.position = candle.close
        self.interval = atr
        self.ma = ma
        self.sequence = 1 if candle.close > candle.open else -1






from datetime import datetime


class Candle:

    def __init__(self,
                 date,
                 open,
                 high,
                 low,
                 close,
                 volume,
                 tr=None):

        self.date = datetime.strptime(
                    date,
                    "%Y-%m-%dT%H:%M:%S.000000000Z")
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

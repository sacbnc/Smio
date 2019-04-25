import py.api as api

class Stream:
    @property
    def name(self):
        return "%s" %(self.__class__.__name__)

    def get_candles(self, n):
        self.logger.log_info(self.name, "Retrieiving %d candles" % n)
        try:
            return api.get_candles(self.instrument, self.granularity, n)
        except Exception as err:
            self.logger.log_fail(self.name, "Failed getting candles: %s" % err)
            return None

    def get_candle(self):
        while True:
            try:
                new_candle = api.get_last_candle(self.instrument, self.granularity)

                return new_candle
            except Exception as err:
                self.logger.log_fail(self.name, "Failed getting candle: %s" % err)

    def __init__(self, logger):
        self.logger = logger
        self.logger.log_info(self.name, "Starting...")

        self.instrument = logger.instrument
        self.granularity = logger.granularity
        self.candle = None

        startup_str = "Started successfully with: parameters: instrument=%s, granularity=%d" \
                      % (self.instrument, self.granularity)
        self.logger.log_info(self.name, startup_str)



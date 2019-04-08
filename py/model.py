from py.state import State
import py.utilities as utils


class Model:
    @property
    def name(self):
        return "%s %s" %(self.__class__.__name__, self.id)

    def input(self, candle):
        self.candles.pop(0)
        self.candles.append(candle)

        atr = utils.get_candles_atr(self.candles[-self.atr_len:],
                                    last_atr=self.state.interval)

        ma = utils.get_candles_ema(self.candles[-self.ma_len:])

        if self.state.update(candle, atr, ma):
            self.logger.log_info(self.name, "State changed on update, new sequence is %s" % self.state.sequence)
            return self.state

        self.logger.log_info(self.name, "Updated model with no state change")
        return None


    """
    __init__
    Initialise the model by first forming the ATR and MA from the
    first minimum needed number of candles, then update the model's
    state for each remaining candle. 
    """
    def __init__(self, id, output, logger, init_candles, atr_len, ma_len, continuation=1, reversal=2):
        self.id = id
        self.output = output
        self.logger = logger

        # increment atr_len by 1 so first
        # can be used to calculate the TR
        self.atr_len = atr_len + 1
        self.ma_len = ma_len


        self.continuation = continuation
        self.reversal = reversal

        # check number of candles is enough to build
        if len(init_candles) < max(self.atr_len, self.ma_len):
            raise Exception(len(init_candles), "is not enough to build model")

        # the number of candles needed to create ATR and MA
        self.retention = max(self.atr_len, self.ma_len)
        self.candles = init_candles[0:self.retention]

        atr = utils.get_candles_atr(init_candles[-self.atr_len:])
        ma = utils.get_candles_ema(init_candles[-self.ma_len:])

        self.state = State(init_candles[self.retention-1], atr, ma, self.continuation, self.reversal)

        for candle in init_candles[self.retention:]:
            self.input(candle)

        self.logger.log_info(self.name, "Model built")

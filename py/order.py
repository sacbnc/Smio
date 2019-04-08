import json

class Order:

    def __init__(self, direction, open, tp, sl, trl):
        self.open_str = "open"
        self.tp_str = "take_profit"
        self.sl_str = "stop_loss"
        self.trl_str = "trailing_stop"

        self.direction = direction
        self.open = open
        self.tp = tp
        self.sl = sl
        self.trl = trl
from py.order import Order


class Intelligence():
    @property
    def name(self):
        return "%s %s" %(self.__class__.__name__, self.id)

    def buy_order(self, state):
        open = state.level(self.distance)
        tp = round(state.level(self.distance + self.tp), 5) if self.tp else self.tp
        sl = round(state.level(self.distance - self.sl), 5) if self.sl else self.sl
        trl = round(open - sl, 5) if self.trl else self.trl

        return Order(1, open, tp, sl, trl)

    def sell_order(self, state):
        open = state.level(-self.distance)
        tp = round(state.level(-self.distance - self.tp), 5) if self.tp else self.tp
        sl = round(state.level(-self.distance + self.sl), 5) if self.sl else self.sl
        trl = round(sl - open, 5) if self.trl else self.trl

        return Order(-1, open, tp, sl, trl)

    def get_order(self, state):
        return self.buy_order(state) if state.up else self.sell_order(state)

    def input(self, state):
        if abs(state.sequence) < self.min_seq:
            self.logger.log_info(self.name, "Order not populated, seq abs(%d) < min seq %d" %(state.sequence, self.min_seq))
            return False, None

        if self.use_mac and not state.mac:
            self.logger.log_info(self.name, "Order not populated, price is on the wrong side of the MA")
            return None

        self.logger.log_info(self.name, "Order populated")
        return self.get_order(state)

    def __init__(self, id, output, logger, distance, tp, sl, trl, min_seq, use_mac):
        self.logger = logger
        self.output = output
        self.id = id

        self.distance = distance
        self.tp = round(tp, 5) if tp > 0 else None
        self.sl = round(sl, 5) if sl > 0 else None
        self.trl = round(trl, 5) if trl > 0 else None
        self.min_seq = min_seq

        # moving average composition
        # is the up sequence above the ma
        # is the down sequence below the ma
        self.use_mac = use_mac

        self.logger.log_info(self.name, "Intelligence started")

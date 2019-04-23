from py.order import Order


class Intelligence():
    @property
    def name(self):
        return "%s %s" %(self.__class__.__name__, self.id)

    def buy_order(self, state):
        open = round(state.level(self.distance), 5)
        tp = round(state.level(self.distance + self.tp), 5) if self.tp else self.tp
        sl = round(state.level(self.distance - self.sl), 5) if self.sl else self.sl
        trl = round(open - sl, 5) if self.trl else self.trl

        return Order(self.name, 1, open, tp, sl, trl)

    def sell_order(self, state):
        open = round(state.level(-self.distance), 5)
        tp = round(state.level(-self.distance - self.tp), 5) if self.tp else self.tp
        sl = round(state.level(-self.distance + self.sl), 5) if self.sl else self.sl
        trl = round(sl - open, 5) if self.trl else self.trl

        return Order(self.name, -1, open, tp, sl, trl)

    def get_order(self, state):
        return self.buy_order(state) if state.up else self.sell_order(state)

    def input(self, state):
        if abs(state.sequence) < self.min_seq:
            self.logger.log_info(self.name, "Order not populated, seq abs(%d) < min seq %d" %(state.sequence, self.min_seq))
            return None

        if self.use_mac and not state.mac:
            self.logger.log_info(self.name, "Order not populated, price is on the wrong side of the MA")
            return None

        order = self.get_order(state)
        update_str = "Order populated: open=%f, tp=%f, sl=%f, trl=%f" \
                     % (order.open, order.tp, order.sl, order.trl)
        self.logger.log_info(self.name, update_str)

        return order

    def __init__(self, id, output, logger, distance, tp, sl, trl, min_seq, use_mac):
        self.id = id
        self.output = output
        self.logger = logger
        self.logger.log_info(self.name, "Starting...")

        self.distance = distance
        self.tp = round(tp, 5)
        self.sl = round(sl, 5)
        self.trl = round(trl, 5)
        self.min_seq = min_seq
        self.use_mac = use_mac

        startup_str = "Started successfully with parameters: distance=%d, tp=%d, sl=%d, trl=%d, min_seq=%d" \
                      % (distance, tp, sl, trl, min_seq)
        logger.log_info(self.name, startup_str)

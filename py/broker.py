import py.api as api


class Broker:
    @property
    def name(self):
        return "%s %s" %(self.__class__.__name__, self.id)

    def get_units(self):
        return 8000

    def input(self, order):
        units = self.get_units()
        units = -units if order.direction == -1 else units

        try:
            update_message = "Received order proposal: units=%d, open=%f, tp=%f, sl=%f, trl=%f" \
                             % (units, order.open, order.tp, order.sl, order.trl)
            self.logger.log_info(self.name, update_message)
        except Exception:
            self.logger.log_fail(self.name, "Received order with undeclared field(s) (None)")
            return False

        trade_id, error_message = api.place_order(api.get_context(),
                                                  self.account,
                                                  self.instrument,
                                                  units,
                                                  round(order.open, 5),
                                                  round(order.tp, 5),
                                                  round(order.sl, 5),
                                                  round(order.trl, 5))

        if error_message:
            self.logger.log_fail(self.name, "Order failed for %s with error: %s" % (order.author, error_message))
            return False

        self.logger.log_info(self.name, "Order %s placed for %s" % (trade_id, order.author))
        return True

    def __init__(self, id, logger, risk, account):
        self.id = id
        self.logger = logger
        self.logger.log_info(self.name, "Starting...")

        self.risk = risk
        self.instrument = logger.instrument
        self.account = account

        startup_str = "Started successfully with: parameters: risk=%d, account=%s" \
                      % (risk, account)
        self.logger.log_info(self.name, startup_str)


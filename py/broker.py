import py.api as api


class Broker:
    @property
    def name(self):
        return "%s %s" %(self.__class__.__name__, self.id)

    def get_units(self):
        return 1000

    def input(self, order):
        units = self.get_units()
        units = -units if order.direction == -1 else units

        self.logger.log_info(self.name,"Received order: units=%d, open=%f, tp=%f, sl=%f, trl=%f"
                             % (units, order.open, order.tp, order.sl, order.trl))

        trade_id, error_message = api.place_order(api.get_context(),
                                                  self.account,
                                                  self.instrument,
                                                  units,
                                                  order.open,
                                                  order.tp,
                                                  order.sl,
                                                  order.trl)

        if error_message:
            self.logger.log_fail(self.name, "Order failed: %s" % error_message)
            return False

        self.logger.log_info(self.name, "Order placed: %s" % trade_id)
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


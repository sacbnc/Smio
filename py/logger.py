import datetime
import datetime
import py.utilities as utils


class Logger():

    info = 'INFO'
    warn = 'WARN'
    fail = 'FAIL'

    insert_sql = "INSERT INTO LOG (ts, implementation, instrument, granularity, component, type, message) VALUES " \
                 "(now(),'{:}','{:}','{:}','{:}','{:}','{:}')"

    def log_info(self, component, message):
        self.write_log(component, self.info, message)

    def log_warn(self, component, message):
        self.write_log(component, self.warn, message)

    def log_fail(self, component, message):
        self.write_log(component, self.fail, message)

    def write_log(self, component, type, message):
        sql = self.insert_sql.format(self.implementation,
                                     self.instrument,
                                     self.granularity,
                                     component,
                                     type,
                                     message.replace("'", ""))
        utils.write_to_db(sql)

    def __init__(self, implementation, instrument, granularity):
        self.implementation = implementation
        self.instrument = instrument
        self.granularity = granularity



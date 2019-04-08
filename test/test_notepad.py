import py.config as config
from py.logger import Logger
from py.stream import Stream

logger = Logger(0, "EUR_USD", 30)
candles = Stream(logger).get_candles(30)

config.get_models(logger, candles)

config.get_intelligences(logger)

config.get_brokers(logger)

print(config.get_account(logger))



import argparse
import time
import py.config as config
from datetime import datetime
from datetime import timedelta
from py.logger import Logger



"""
Define args
"""

parser = argparse.ArgumentParser()

parser.add_argument("implementation", type=int)
parser.add_argument("instrument")
parser.add_argument("granularity", type=int)

args = parser.parse_args()

"""
Parse args
"""

implementation = args.implementation
instrument = args.instrument
granularity = args.granularity

"""
Create logger and lists of components
"""

logger = Logger(implementation, instrument, granularity)
stream = config.get_stream(logger)
candles = stream.get_candles(config.get_max_model_param(implementation) + 1)
models = config.get_models(logger, candles)
intelligences = config.get_intelligences(logger)
brokers = config.get_brokers(logger)

"""
Functions
"""


def name():
    return "Main %d" % implementation


"""
Main
"""

candle = stream.get_candle()
next_candle = candle
count = 0

while True:

    while next_candle.date == candle.date:
        next_minute = datetime.now().replace(second=1) + timedelta(minutes=1)
        time.sleep((next_minute - datetime.now()).total_seconds())
        next_candle = stream.get_candle()
        print(candle.date, next_candle.date)

    candle = next_candle
    logger.log_info(name(), "Received new candle: %s" % candle.date)

    for model in models:
        state = model.input(candle)

        if state is not None:
            order = intelligences[model.output].input(state)
            print(order.open, candle.close)
            if order is not None:
                brokers[intelligences[model.output].output].input(order)















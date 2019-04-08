import py.utilities as utils
from py.stream import Stream
from py.model import Model
from py.intelligence import Intelligence
from py.broker import Broker

account_sql = "SELECT * FROM account_config WHERE implementation = %d"
model_sql = "SELECT * FROM model_config WHERE implementation = %d ORDER BY id;"
intelligence_sql = "SELECT * FROM intelligence_config WHERE implementation = %d ORDER BY id;"
broker_sql = "SELECT * FROM broker_config WHERE implementation = %d ORDER BY id;"

max_atr_sql = "SELECT MAX(atr) FROM model_config WHERE implementation = %d;"
max_ma_sql = "SELECT MAX(ma) FROM model_config WHERE implementation = %d;"

def get_account(logger):
    # TODO: error on more than one account
    return utils.read_db(account_sql % logger.implementation)[0][1]

def get_max_model_param(implementation):
    max_atr = utils.read_db(max_atr_sql % implementation)
    max_ma = utils.read_db(max_ma_sql % implementation)

    return max(max_atr[0][0], max_ma[0][0])

def get_stream(logger):
    return Stream(logger)

def get_models(logger, candles):
    tuples = utils.read_db(model_sql % logger.implementation)

    models = []
    for t in tuples:
        models.append(Model(t[0],
                            t[2],
                            logger,
                            candles,
                            t[3],
                            t[4],
                            t[5],
                            t[6]))

    return models


def get_intelligences(logger):
    tuples = utils.read_db(intelligence_sql % logger.implementation)

    intelligences = []
    for t in tuples:
        intelligences.append(Intelligence(t[0], t[2], logger, t[3], t[4], t[5], t[6], t[7], t[8]))

    return intelligences


def get_brokers(logger):
    account = get_account(logger)
    tuples = utils.read_db(broker_sql % logger.implementation)

    brokers = []
    for t in tuples:
        brokers.append(Broker(t[0], logger, t[2], account))

    return brokers








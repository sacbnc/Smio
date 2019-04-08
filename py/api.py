import v20
import py.utilities as utils
from py.candle import Candle
from order.view import print_order_create_response_transactions

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 CONSTANTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

S5 = 5
S30 = 30
M1 = 60
M5 = 300
M15 = 900
M30 = 1800
H1 = 3600
H4 = 14400
D1 = 86400

granularity_strings = {S5:  "S5",
                       S30: "S30",
                       M1:  "M1",
                       M5:  "M5",
                       M15: "M15",
                       M30: "M30",
                       H1:  "H1",
                       H4:  "H4",
                       D1:  "D"}

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 MISC 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_context():
    return v20.Context(
        "api-fxpractice.oanda.com",
        443,
        token="3c53123249585461404e186806c665ec-2314f605c352d944327e1bfe2e5451c5"
    )

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 CANDLES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def parse_candle_response(response):
    c = getattr(response, "mid", None)
    return Candle(response.time, c.o, c.h, c.l, c.c, response.volume)


def get_candles(instrument,
                granularity,
                count):
    api_context = get_context()

    granularity = granularity_strings[granularity]

    response = api_context.instrument.candles(instrument=instrument,
                                              granularity=granularity,
                                              count=count)

    candles = []
    try:
        for candle in response.get("candles", 200):
            candles.append(parse_candle_response(candle))
    except Exception:
        raise Exception(response.get(field="errorMessage"))

    return candles


def get_last_candle(instrument, granularity):
    return get_candles(instrument, granularity, 1)[0]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ORDERS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def place_order(context,
                account_id,
                instrument,
                units,
                open,
                take_profit,
                stop_loss,
                trailing_stop):

    if take_profit is not None:
        take_profit = v20.transaction.TakeProfitOrderTransaction(price=take_profit)

    if stop_loss is not None:
        stop_loss = v20.transaction.StopLossOrderTransaction(price=stop_loss)
    if trailing_stop is not None:
        trailing_stop = v20.transaction.TrailingStopLossOrderTransaction(distance=trailing_stop)

    response = context.order.limit(accountID=account_id,
                                   instrument=instrument,
                                   units=units,
                                   price=open,
                                   takeProfitOnFill=take_profit,
                                   stopLossOnFill=stop_loss,
                                   trailingStopLossOnFill=trailing_stop)

    return parse_response(response)


def parse_response(response):
    """
    Return trade_id and error_message, populating only the value
    that is present in the response.
        A successful order returns <order_id> and None
        A failed order return None and <error_message>
    :return trade_id, error message
    """
    try:
        # Attempt to get errorMessage if response is an error
        # If not, drop down into parsing a successful response
        return None, response.get(field="errorMessage")
    except Exception:
        return response.get(field="lastTransactionID"), None

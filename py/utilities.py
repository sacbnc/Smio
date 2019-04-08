import math
import pandas as pd
import psycopg2 as postgres

# Misc

def format_date(date):
    return ("%s.000000000Z" % date).replace(" ", "T")

def normal_round(n):
    # make a multiplier so odd numbers can be
    # calculated in same way
    m = 1 if n > 0 else -1
    n = abs(n)

    if n - math.floor(n) < 0.5:
        return math.floor(n) * m
    return math.ceil(n) * m



# ATR

def get_candles_atr(candles, last_atr=None):
    tr_values = []

    for i in range(1,len(candles)):
        tr_values.append(get_tr(candles[i-1], candles[i]))

    return get_atr(tr_values, last_atr)

def get_atr(tr_values, last_atr=None):
    tr_avg = sum(tr_values) / len(tr_values)

    if last_atr is not None:
        tr_avg *= (len(tr_values) - 1)
        tr_avg += last_atr
        tr_avg /= len(tr_values)

    return float("{0:.5f}".format(tr_avg))

def get_tr(old_candle, new_candle):
    return max(abs(new_candle.high - new_candle.low),
               abs(new_candle.high - old_candle.close),
               abs(new_candle.low - old_candle.close))


# MA

def get_ema(values):
    df = pd.DataFrame(values)

    return df.ewm(span=len(values), adjust=False).mean().iloc[1][0]


def get_candles_ema(candles):
    values = []
    for candle in candles:
        values.append(candle.close)

    return get_ema(values)


# Database

def get_db_connection(host="localhost", database="wfcm", user="postgres", password="postgres"):
    return postgres.connect(host=host, database=database, user=user, password=password)

def write_to_db(sql):
    conn = get_db_connection()
    conn.cursor().execute(sql)
    conn.commit()

def read_db(sql):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)

    return cursor.fetchall()




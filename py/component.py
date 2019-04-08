import datetime as datetime

class Component:




    def __init__(self, instrument, output):
        self.instrument = instrument
        self.output = output





    def write_to_db(run_id, acc_start, acc_end, min_seq, mac, tp_bricks, sl_bricks, trl_bricks, database, lowest,
                    highest):
        sql = ("INSERT INTO RUN_META VALUES ({:d},{:d},{:f},{:d},'{:}',{:d},{:d},{:d},{:f},{:f})"
               .format(run_id,
                       acc_start,
                       acc_end,
                       min_seq,
                       mac,
                       tp_bricks if tp_bricks is not None else 0,
                       sl_bricks if sl_bricks is not None else 0,
                       trl_bricks if trl_bricks is not None else 0,
                       lowest,
                       highest))

        conn = data.get_db_connection(database=database)
        data.write_to_db(sql, conn)
        conn.close()



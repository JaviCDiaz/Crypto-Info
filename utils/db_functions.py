import sqlite3
from sqlite3 import Error


# UPDATE TALBE
def db_update_table (db_conn, db_table_name, coin_updated_info):
    db_conn.cursor().execute(f'''
        UPDATE {db_table_name}
        SET
            price = {coin_updated_info['price']},
            volume_24h = {coin_updated_info['volume_24h']},
            quote_volume_24h = {coin_updated_info['quote_volume_24h']},
            change_24h = {coin_updated_info['change_24h']},
            chart_7d = "{coin_updated_info['chart_7d']}"
        WHERE
            coin = "{coin_updated_info['coin']}" AND exchange = "{coin_updated_info['exchange']}"
    ''')


# CREATE TABLE
def db_create_table (db_conn, db_table_name):
    db_conn.cursor().execute(f'''
            CREATE TABLE IF NOT EXISTS {db_table_name}(
                [coin] TEXT,
                [exchange] TEXT,
                [price] FLOAT,
                [volume_24h] FLOAT,
                [quote_volume_24h] FLOAT,
                [change_24h] FLOAT,
                [chart_7d] TEXT,
                UNIQUE (coin, exchange)
            )
        ''')


# FUNCTION TO ADD COIN TO DB
def add_coin_to_db (db_path, db_table_name, info):
    conn = None
    success = False
    try:
        conn = sqlite3.connect(db_path)

        db_create_table(conn, db_table_name)

        conn.cursor().execute(f'''
            INSERT OR IGNORE INTO {db_table_name} (coin, exchange, price, volume_24h, quote_volume_24h, change_24h, chart_7d)
            VALUES ("{info['coin']}", "{info['exchange']}", {info['price']}, {info['volume_24h']}, {info['quote_volume_24h']}, {info['change_24h']}, "{info['chart_7d']}")
        ''')
                            
        conn.commit()
        success = True

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

    return success
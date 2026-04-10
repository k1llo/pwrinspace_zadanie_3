import psycopg2


def init_connection(db_url):
    return psycopg2.connect(db_url)


def init_db(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data BYTEA NOT NULL
            )
            """
        )
    conn.commit()


def insert_telemetry(conn, payload):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO telemetry (data) VALUES (%s)",
            (psycopg2.Binary(payload),),
        )
    conn.commit()
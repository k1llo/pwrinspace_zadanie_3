import psycopg2


def init_connection(db_url):
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    return conn


def init_db(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                sender VARCHAR(50) NOT NULL,
                text TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data BYTEA NOT NULL
            )
            """
        )


def fetch_recent_telemetry(conn, limit: int = 30):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT timestamp, data FROM telemetry ORDER BY id DESC LIMIT %s",
            (limit,),
        )
        return cur.fetchall()


def fetch_messages(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT sender, text FROM messages ORDER BY id ASC")
        return cur.fetchall()


def insert_message(conn, sender, text):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO messages (sender, text) VALUES (%s, %s)",
            (sender, text),
        )
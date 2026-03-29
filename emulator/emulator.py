import os
import time
import random
import psycopg2
import krzysiu_pb2

DB_URL = os.environ.get("DB_URL")

def init_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data BYTEA NOT NULL
            )
        """)
    conn.commit()

def main():
    time.sleep(5) # Waitin just to make sure that posgres is up
    
    conn = psycopg2.connect(DB_URL)
    init_db(conn)
    
    print("Emulator started. Sending data to Krzysiu")
    
    while True:
        # Generate random data
        vitals = krzysiu_pb2.VitalSigns()
        vitals.energy = random.randint(40, 100)
        vitals.heart_rate = random.randint(70, 130)
        vitals.temperature = round(random.uniform(36.0, 37.5), 1)
        vitals.mood = "Zadowolony" if vitals.energy > 60 else "Zmęczony"
        
        binary_data = vitals.SerializeToString()
        
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO telemetry (data) VALUES (%s)",
                (psycopg2.Binary(binary_data),)
            )
        conn.commit()
        
        time.sleep(2)

if __name__ == "__main__":
    main()
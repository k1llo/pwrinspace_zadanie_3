import os
import random
import pandas as pd
import psycopg2
import streamlit as st
import krzysiu_pb2

st.set_page_config(page_title="Centrum Krzysia", page_icon="🧑🏻‍🚀")

DB_URL = os.environ.get("DB_URL")

@st.cache_resource
def init_connection():
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    return conn

conn = init_connection()

def init_db():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                sender VARCHAR(50) NOT NULL,
                text TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data BYTEA NOT NULL
            )
        """)

init_db()

st.title("🧑🏻‍🚀 Centrum Monitoringu Krzysia")

@st.fragment(run_every="2s")
def render_telemetry():
    st.subheader("📊 Funkcje Życiowe")
    
   
    with conn.cursor() as cur:
        cur.execute("SELECT timestamp, data FROM telemetry ORDER BY id DESC LIMIT 30") # Select last 30 records
        rows = cur.fetchall()
        
    if not rows:
        st.info("No data :( waiting")
        return
        
    # Process data and deserialize Protobuf
    parsed_data = []
    for row in reversed(rows):
        timestamp, binary_data = row
        vitals = krzysiu_pb2.VitalSigns()
        vitals.ParseFromString(binary_data)
        
        parsed_data.append({
            "Time": timestamp.strftime("%H:%M:%S"),
            "Energy": vitals.energy,
            "HeartRate": vitals.heart_rate,
            "Temp": vitals.temperature,
            "Mood": vitals.mood
        })
        
    df = pd.DataFrame(parsed_data)
    latest = df.iloc[-1]
    

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Energia", f"{latest['Energy']} %")
    c2.metric("Tętno", f"{latest['HeartRate']} bpm")
    c3.metric("Temperatura", f"{latest['Temp']} °C")
    c4.metric("Nastrój", latest['Mood'])
    
    st.line_chart(df.set_index("Time")[["Energy", "HeartRate"]])

render_telemetry()

st.divider()


st.subheader("💬 Komunikacja")

with conn.cursor() as cur:
    cur.execute("SELECT sender, text FROM messages ORDER BY id ASC") #Select and show chat history
    chat_rows = cur.fetchall()

for sender, text in chat_rows:
    role = "user" if sender == "Ziemia" else "assistant"
    with st.chat_message(role):
        st.markdown(text)


if prompt := st.chat_input("Napisz wiadomość do Krzysia"):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO messages (sender, text) VALUES (%s, %s)", ("Ziemia", prompt))
        
        replies = ["Zrozumiałem, Ziemio!", "Krzysiu czuje się świetnie.", "Przesyłam pozdrowienia!", "Bajo jajo"]
        reply = random.choice(replies)
        
        cur.execute("INSERT INTO messages (sender, text) VALUES (%s, %s)", ("Krzysiu", reply))
    conn.commit()
    
    st.rerun()
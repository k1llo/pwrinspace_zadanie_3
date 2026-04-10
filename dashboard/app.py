import os
import random
import pandas as pd
import psycopg2
import streamlit as st
import krzysiu_pb2
import db

st.set_page_config(page_title="Centrum Krzysia", page_icon="🧑🏻‍🚀")

DB_URL = os.environ.get("DB_URL")

@st.cache_resource
def get_connection():
    return db.init_connection(DB_URL)

conn = get_connection()
db.init_db(conn)

st.title("🧑🏻‍🚀 Centrum Monitoringu Krzysia")

@st.fragment(run_every="2s")
def render_telemetry():
    st.subheader("📊 Funkcje Życiowe")
    
   
    rows = db.fetch_recent_telemetry(conn)
        
    if not rows:
        st.info("No data :( waiting")
        return
        
    # Process data and deserialize Protobuf
    parsed_data = []
    for timestamp, binary_data in reversed(rows):
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

chat_rows = db.fetch_messages(conn)

for sender, text in chat_rows:
    role = "user" if sender == "Ziemia" else "assistant"
    with st.chat_message(role):
        st.markdown(text)


if prompt := st.chat_input("Napisz wiadomość do Krzysia"):
    with conn.cursor() as cur:
        db.insert_message(conn, "Ziemia", prompt)
        
        replies = ["Zrozumiałem, Ziemio!", "Krzysiu czuje się świetnie.", "Przesyłam pozdrowienia!", "Bajo jajo"]
        reply = random.choice(replies)
        
        db.insert_message(conn, "Krzysiu", reply)
    
    st.rerun()
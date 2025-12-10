import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------
# Database Setup
# --------------------------------------------
conn = sqlite3.connect("mood_journal.db", check_same_thread=False)
c = conn.cursor()

# Create table if not exists
c.execute('''
CREATE TABLE IF NOT EXISTS MoodLogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    log_date TEXT,
    mood TEXT,
    notes TEXT,
    song_link TEXT
)
''')
conn.commit()

# --------------------------------------------
# Song Recommendation Mapping
# --------------------------------------------
song_dict = {
    "Happy": "https://www.youtube.com/watch?v=RIriENOmOpo&list=PL4sNEU2Mgm6bNnbM-qKPmTwwDromFqpMQ",
    "Sad": "https://www.youtube.com/watch?v=VLav-xhWRRA&list=RDVLav-xhWRRA&start_radio=1",
    "Excited": "https://www.youtube.com/watch?v=Fa4COn3sPDY&list=PLxtK6ShTG4WXy2w8KiCi3hg1jjY-R2xQL",
    "Stressed": "https://www.youtube.com/watch?v=DDb7OILQMMA&list=PL46rzuOyy5dbZzjKjukcDA21e9tUEuloZ",
    "Calm": "https://www.youtube.com/watch?v=XZGTTLiWRXg&list=PLHStem9c0rLJcEdqYJeFRDD33k8HQtFPY"
}

# --------------------------------------------
# Streamlit App
# --------------------------------------------
st.title("🎵 Mood Based Music Recommender")
sst.write("-----------")
st.write("Hellooooooooooooooooooo buddy")
st.write("Log how you feel, uncover mood patterns, and enjoy personalized playlists!")
# User Input Section
user_name = st.text_input("Enter your name:")
mood = st.selectbox("How is your Mood today?", ["Happy", "Sad", "Excited", "Stressed", "Calm"])
notes = st.text_area("Optional notes:")

if st.button("Save your Feeling"):
    if user_name.strip() == "":
        st.error("Hello buddy.... Please enter your name before saving.")
    else:
        today = str(date.today())
        song_link = song_dict[mood]

        c.execute("INSERT INTO MoodLogs (user_name, log_date, mood, notes, song_link) VALUES (?,?,?,?,?)",
                (user_name, today, mood, notes, song_link))
        conn.commit()

        st.success(f"I gotchhhha! Here's your recommended song: 🎵 [Listen Here]({song_link})")


# --------------------------------------------
# Mood History & Analytics
# --------------------------------------------
st.subheader("📊 Basic Analysis of Your Feelings")

if user_name.strip() != "":
    df = pd.read_sql("SELECT * FROM MoodLogs WHERE user_name=?", conn, params=(user_name,))

    if not df.empty:
        st.write("### Your Mood Entries:")
        st.dataframe(df[['log_date', 'mood', 'notes', 'song_link']])

        # Mood Count Visualization
        st.write("### Mood Frequency Chart")

        fig, ax = plt.subplots(figsize=(6,4))
        sns.countplot(data=df, x="mood", palette="viridis", ax=ax)
        plt.title("Mood Frequency")
        st.pyplot(fig)

        # Mood Trend
        st.write("### Mood Trend Over Time")
        df['log_date'] = pd.to_datetime(df['log_date'])
        mood_map = {"Happy":5, "Excited":4, "Calm":3, "Sad":2, "Stressed":1}
        df['mood_score'] = df['mood'].map(mood_map)

        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.plot(df['log_date'], df['mood_score'], marker='o')
        ax2.set_title("Mood Trend")
        ax2.set_ylabel("Mood Score (1–5)")
        ax2.set_xlabel("Date")
        st.pyplot(fig2)

    else:
        st.info("No mood entries found. Start by logging your first mood!")
else:
    st.info("Enter your name to view your mood history.")

st.markdown("---")
st.write("Made with ❤️ using Python & Streamlit")

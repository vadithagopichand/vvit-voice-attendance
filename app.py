from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
import sqlite3

app = Flask(__name__)

# ============================================================
# TWILIO SETTINGS
# ============================================================
import os

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

TWILIO_NUMBER = "+17372508034"

# Your current Pinggy public URL
PUBLIC_URL = "https://vvit-voice-attendance-1.onrender.com"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ============================================================
# DATABASE
# ============================================================

def save_response(phone, reason):
    connection = sqlite3.connect("attendance.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            reason TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO attendance (phone, reason) VALUES (?, ?)",
        (phone, reason)
    )

    connection.commit()
    connection.close()


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return """
    <h2>VVIT College AI Voice Agent</h2>
    <p>Voice Agent is running successfully!</p>
    <form action="/make-call" method="POST">
        <label>Parent Phone Number:</label><br><br>
        <input type="text" name="phone"
               placeholder="+91XXXXXXXXXX"
               required>
        <br><br>
        <button type="submit">Call Parent</button>
    </form>
    """


# ============================================================
# MAKE PHONE CALL
# ============================================================
@app.route("/make-call", methods=["GET", "POST"])
def make_call():

    parent_number = "+918019617631"

    try:
        call = client.calls.create(
            to=parent_number,
            from_=TWILIO_NUMBER,
            url=PUBLIC_URL + "/voice"
        )

        return f"""
        <h2>Call Started Successfully!</h2>
        <p>Calling: {parent_number}</p>
        <p>Call SID: {call.sid}</p>
        """

    except Exception as e:
        return f"""
        <h2>Call Failed</h2>
        <p>{e}</p>
        """
app.run(host="0.0.0.0", port=5000)

















import sqlite3
import os
import openai
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from utilities import get_id

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
openai.api_key = os.getenv("OPENAI_API_KEY")


def startup():
    conn = sqlite3.connect("data.db")
    conn.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    conv_id TEXT (50),
    role TEXT (12),
    content TEXT,
    total_tokens INTEGER (16)
)""")
    conn.commit()
    conn.close()


@app.route('/')
def mainpage():
    return render_template('index.html')

# Handle sent messages
@socketio.on('user_message')
def handle_message(data):
    conn = sqlite3.connect("data.db")
    conn.execute("INSERT INTO contents (conv_id, content_id, role, content) VALUES (?, ?, ?, ?)", ('000000', get_id(), data['role'], data['msg']))
    conn.commit()
    conn.close()
    emit('user_message2', {'role': data['role'], 'msg': data['msg']}, broadcast=True)

@socketio.on('get_chat_box_contents')
def get_chat_box_contents(data):
    conn = sqlite3.connect("data.db")
    result = conn.execute(f"SELECT * FROM contents WHERE conv_id='{data['''conv_id''']}'").fetchall()
    conn.close()
    emit('get_chat_box_contents2', result)

if __name__ == '__main__':
    startup()
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)

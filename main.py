import sqlite3
import os
from unittest import result
import openai
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from utilities import get_new_content_id, get_new_conv_id

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
openai.api_key = os.getenv("OPENAI_API_KEY")


def startup():
    conn = sqlite3.connect("data.db")
    conn.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    conv_id TEXT (6) PRIMARY KEY UNIQUE,
    conv_desc TEXT
);""")
    conn.commit()
    conn.execute("""
CREATE TABLE IF NOT EXISTS contents (
    conv_id TEXT (6) REFERENCES conversations (conv_id),
    content_id TEXT (6),
    role TEXT (12),
    content TEXT,
    total_tokens INTEGER (16) 
);""")
    conn.commit()
    conn.close()


@app.route('/')
def mainpage():
    return render_template('index.html')


@socketio.on('user_message')
def user_input(data):
    conn = sqlite3.connect("data.db")
    if data['conv_id'] == '999999':
        msg_conv_id = get_new_conv_id()
        conn.execute(
            "INSERT INTO conversations (conv_id) VALUES (?)", (msg_conv_id,))
        conn.commit()
    else:
        msg_conv_id = data['conv_id']
    conn.execute("INSERT INTO contents (conv_id, content_id, role, content) VALUES (?, ?, ?, ?)",
                 (msg_conv_id, get_new_content_id(msg_conv_id), data['role'], data['msg']))
    conn.commit()
    conn.close()
    emit('user_message2', {'conv_id': msg_conv_id, }, broadcast=True)


@socketio.on('get_convs')
def get_convs():
    conn = sqlite3.connect("data.db")
    result = conn.execute(f"SELECT * FROM conversations").fetchall()
    conn.close()
    emit('get_convs2', result)


@socketio.on('get_chat_box_contents')
def get_chat_box_contents(data):
    conn = sqlite3.connect("data.db")
    result = conn.execute(
        f"SELECT * FROM contents WHERE conv_id='{data['''conv_id''']}'").fetchall()
    conn.close()
    emit('get_chat_box_contents2', result)


if __name__ == '__main__':
    startup()
    socketio.run(app, debug=True)

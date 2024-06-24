from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    emit('user_list', json.dumps(users))


@socketio.on('set_username')
def handle_set_username(username):
    users[request.sid] = username
    emit('user_list', json.dumps(users), broadcast=True)


@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, 'Anonymous')
    message_data = {'username': username, 'message': msg}
    send(message_data, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    users.pop(request.sid, None)
    emit('user_list', json.dumps(users), broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)

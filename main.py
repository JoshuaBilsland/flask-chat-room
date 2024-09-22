import random
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
socketio = SocketIO(app)  # Create server


@app.route('/', methods=['GET', 'POST'])
def home():
    if "create" in request.form:
        return render_template("chat.html")
    return render_template("home.html")


if __name__ == "__main__":
    socketio.run(app)

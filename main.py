import random
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
socketio = SocketIO(app)  # Create server
rooms = []


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        code = request.form["room-code"]

        if not username:
            abort(400, description="A username must be given.")

        if "join" in request.form:
            if code in rooms:
                return redirect(url_for("chat", username, code=code))
            else:
                abort(404, description="Room does not exist. Please check the code or create a new room.")
        elif "create" in request.form:
            code = str(random.randint(100000, 999999))
            rooms.append(code)
            return redirect(url_for("chat", username=username, code=code))
    else:
        return render_template("home.html")


@app.route("/chat/<code>/<username>")
def chat(code, username):
    return render_template("chat.html", code=code, username=username)


@socketio.on("join")
def on_join(data):
    username = data["username"]
    code = data["room-code"]
    join_room(code)
    send(f"{username} has joined the room.", to=code)


@socketio.on("leave")
def on_leave(data):
    username = data["username"]
    code = data["room-code"]
    leave_room(code)
    send(f"{username} has left the room.", to=code)


@socketio.on("message")
def handle_message(data):
    code = data["room-code"]
    send({"msg": data["msg"], "username": data["username"], "time": data["time"]}, to=code)


if __name__ == "__main__":
    socketio.run(app)

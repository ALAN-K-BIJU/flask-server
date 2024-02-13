from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import random
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

cors = CORS(app, resources={r"/socket.io/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

def emit_updated_data():
    while True:
        colors = ["#FF0000", "#00FF00", "#00FF00", "#FF0000"] 
        random.shuffle(colors)  

        data = {
            "light1": colors[0],
            "light2": colors[1],
            "light3": colors[2],
            "light4": colors[3],
        }

        socketio.emit("lights_update", data, namespace='/')
        socketio.sleep(7)

@socketio.on('connect')
def connected():
    sid = request.sid
    print(sid)
    print("Client is connected.")

    threading.Thread(target=emit_updated_data, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)

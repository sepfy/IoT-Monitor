#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

import threading
import time
import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

params = {
	'ping_timeout': 10,
	'ping_interval': 5
}

socketio = SocketIO(app, **params)

@app.route('/')
def index():
    return render_template('index.html')

sids = []
def emit_iot():
  while True:
    for sid in sids:
      socketio.emit("update", {"data": [str(datetime.datetime.now()), 20+random.random()], "sid": sid}, namespace='/message', room=sid)
    time.sleep(3)
  

@socketio.on('connect', namespace='/message')
def test_connect():
    sids.append(request.sid)
    print(request)
    print(session)
    emit('status', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/message')
def test_disconnect():
    sids.remove(request.sid)
    print('Client disconnected')
    print(sids)





if __name__ == '__main__':
  t = threading.Thread(target = emit_iot)
  t.start()
  socketio.run(app, host='0.0.0.0')
  t.join()

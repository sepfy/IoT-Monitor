#!/usr/bin/env python
from flask import Flask, render_template, session, request, redirect, url_for
from flask_login import LoginManager
from flask_socketio import SocketIO, emit
import json
from forms import LoginForm
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
  def __init__(self):
    DefaultDelegate.__init__(self)

  def handleDiscovery(self, dev, isNewDev, isNewData):
    if isNewDev:
      socketio.emit("update", dev.addr, namespace='/message', room=sid)


#from model import Model
'''
model = Model()
'''

from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user  


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

login_manager = LoginManager()
login_manager.setup_app(app)
@login_manager.user_loader
def user_loader(username):
  user = User()
  return user

class User(UserMixin):  
  pass 

socketio = SocketIO(app, **params)

@app.route('/')
@login_required
def index():
  return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():

  form = LoginForm()
  if form.validate_on_submit():
    user = User()
    user.id = form.username.data
    login_user(user)
    return redirect("/")

  return render_template("login.html", form=form)

@login_manager.unauthorized_handler
def unauthorized():
  return redirect("/login")

@app.route('/logout')  
@login_required
def logout():  
  logout_user()  
  return redirect("/login")

@app.route('/device', methods=['GET', 'POST'])
@login_required
def device():

    '''
    if request.method == "POST": 
        print(request.values["key"])

    if request.args.get("id"):
      devid = request.args.get("id")
      print(devid)
      temp = model.get_4hour("t")
      humi = model.get_4hour("h")
    
      return render_template('device.html', temp=temp, humi=humi)
    '''
    return render_template('device_list.html')

@app.route('/setting')
@login_required
def setting():
    return render_template('setting.html')

sids = []
def emit_iot():
  scanner = Scanner().withDelegate(ScanDelegate())
  devices = scanner.scan(10.0)
  #while True:
  #  #msg = model.get_last()
  #  #print(msg)
  #  msg = {"temp": 20+round(random.random(),2), "humi": 67}
  #  #for sid in sids:
  #  #  socketio.emit("update", {"data": json.dumps(msg), "sid": sid}, namespace='/message', room=sid)
  #  #time.sleep(3)
  

@socketio.on('connect', namespace='/message')
def test_connect():
    sids.append(request.sid)
    #print(request)
    #print(session)
    emit('status', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/message')
def test_disconnect():
    sids.remove(request.sid)
    #print('Client disconnected')
    #print(sids)



if __name__ == '__main__':
  t = threading.Thread(target = emit_iot)
  t.start()
  socketio.run(app, host='0.0.0.0')
  t.join()

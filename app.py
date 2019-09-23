#!/usr/bin/env python
from flask import Flask, render_template, session, request, redirect, url_for
from flask_login import LoginManager
from flask_socketio import SocketIO, emit
from forms import LoginForm, ProfileForm, DeviceForm, TypeForm
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user  
from model import LevelDBModel
from central import Central
import threading
import time
import datetime
import random
import json

gattdb = LevelDBModel("devtype")
devdb = LevelDBModel("devinfo")



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

params = {
	'ping_timeout': 10,
	'ping_interval': 5
}

socketio = SocketIO(app, **params)


login_manager = LoginManager()
login_manager.setup_app(app)
@login_manager.user_loader
def user_loader(username):
  user = User()
  user.id = username
  return user

class User(UserMixin): 
  pass 


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
  devs = devdb.getall()
  if request.method == 'POST':
    print(request.form.getlist('mac')) 
  return render_template('device_list.html', devs=devs)


@app.route('/device/setting', methods=['GET', 'POST'])
@login_required
def device_setting():
  form = DeviceForm()
  if form.validate_on_submit():
    devdb.modify_dict(form.deviceid.data, "location", form.location.data)
    return redirect("/device")
  return render_template('device.html', form=form)


@app.route('/device/deletion', methods=['GET', 'POST'])
@login_required
def device_deletion():
  devid = request.args.get('id')
  devdb.delete(devid)
  return redirect("/device")


@app.route('/setting')
@login_required
def setting():
  return redirect("/setting/gatt")


@app.route('/setting/profile', methods=['GET', 'POST'])
@login_required
def setting_profile():
  form = ProfileForm()
  if form.validate_on_submit():
    pass
  return render_template('setting/profile.html', form=form)


@app.route('/setting/gatt', methods=['GET', 'POST'])
@login_required
def setting_gatt():
  gatts = gattdb.getall()
  return render_template('setting/gatt.html', gatts=gatts)

@app.route('/setting/gatt/add', methods=['GET', 'POST'])
@login_required
def setting_gatt_add():
  form = TypeForm()
  if form.validate_on_submit():
    services = []

    for service in form.services.data:
      characs = []
      for charac in service["characs"]:
        characs.append({"uuid": charac["uuid"], "desc": charac["desc"]})
      services.append({"uuid": service["uuid"], "characs": characs})

    gattdb.put_dict(form.name.data, services)

    return redirect("/setting")
  return render_template('setting/gatt_add.html', form=form)

@app.route('/setting/gatt/deletion', methods=['GET', 'POST'])
@login_required
def setting_gatt_deletion():
  gattid = request.args.get('id')
  gattdb.delete(gattid)
  return redirect("/setting/gatt")


def scanner_callback(dev):
  obj = {"mac": dev.addr, "type": dev.getValueText(9) , "rssi": dev.rssi}
  socketio.emit("scan", json.dumps(obj), namespace='/scan')


def collector_callback(msg):
  socketio.emit("update", {"data": msg}, namespace='/current')

central = Central(devdb, gattdb, scanner_callback, collector_callback)
tlisten = threading.Thread(target = central.listen)
tlisten.start()
tcollect = threading.Thread(target = central.collect)
tcollect.start()


@socketio.on("connect", namespace="/current")
def scan_connect():
  pass

@socketio.on("disconnect", namespace="/current")
def scan_disconnect():
  pass


@socketio.on("add", namespace="/scan")
def add_devices(msg):
  devdb.put_dict(msg["devid"], {"location": "Bedroom", "type": msg["type"]})

@socketio.on("connect", namespace="/scan")
def scan_connect():
  tscan = threading.Thread(target = central.scan)
  tscan.start()
  
@socketio.on("disconnect", namespace="/scan")
def scan_disconnect():
  tlisten = threading.Thread(target = central.listen)
  tlisten.start()

if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0')
  

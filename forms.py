import json
import plyvel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from model import LevelDBModel

db = LevelDBModel('account/')
db.put("admin", "123456")


class LoginForm(FlaskForm):
  username = StringField('Username')#, validators=[DataRequired()])
  password = PasswordField('Password')#, validators=[DataRequired()])

  def validate(self):
    password = db.get(self.username.data)
    if password is not None:
      if self.password.data == password:
        return True

    self.error = "Error username or password"
    return False

class ProfileForm(FlaskForm):
  username = StringField('Device ID')
  password1 = PasswordField('Password')#, validators=[DataRequired()])
  password2 = PasswordField('Password again')#, validators=[DataRequired()])
  def validate(self):
    if self.password1.data == self.password2.data:
      db.put(self.username.data, self.password1.data)
      return True

    return False


class DeviceForm(FlaskForm):
  location = StringField('Location')
  deviceid = StringField('Device ID')



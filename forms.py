import json
import plyvel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


db = plyvel.DB('account/', create_if_missing=True)
db.put(b"admin", b"123456")


class LoginForm(FlaskForm):
  username = StringField('Username')#, validators=[DataRequired()])
  password = PasswordField('Password')#, validators=[DataRequired()])

  def validate(self):
    bytes_of_username = bytes(self.username.data, encoding = "utf-8")
    bytes_of_password = db.get(bytes_of_username)
    if bytes_of_password is not None:
      password = str(bytes_of_password, encoding = "utf-8")
      if self.password.data == password:
        return True

    self.error = "Error username or password"
    return False

class ProfileForm(FlaskForm):
  password1 = PasswordField('Password')#, validators=[DataRequired()])
  password2 = PasswordField('Password again')#, validators=[DataRequired()])


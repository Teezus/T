from flask.ext.wtf import Form
from wtforms import TextField, validators, PasswordField, SubmitField
from models import User
from werkzeug.security import generate_password_hash

stip_filter = lambda x: x.stip() if x else none

class SigninForm(Form):
  email = TextField("email", [validators.Required("Please enter your email")])
  password = PasswordField('Password', [validators.Required("Please enter your password")])
  submit = SubmitField("Sign In")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False

    user = User.query.filter_by(email=self.email.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid username")
      return False

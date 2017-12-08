from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class NameForm(FlaskForm):
    name = StringField("What's your name?",validators=[DataRequired(), Email()],render_kw = {"placeholder": "Enter Email"})
    submit = SubmitField("Submit")

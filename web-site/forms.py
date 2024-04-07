from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):  # форма для регистрации и логина
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class WriteNoteForm(FlaskForm):  # форма для создания(поиска?) заметки
    is_private = BooleanField('Private')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Write')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):  # форма для регистрации и логина
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class WriteNoteForm(FlaskForm):  # форма для создания(поиска?) заметки
    is_private = BooleanField('Private')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Write')


class ReadNoteForm(FlaskForm):
    search_field = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Register')

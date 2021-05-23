from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField, BooleanField
from wtforms.validators import Email, InputRequired, DataRequired

class LogIn(FlaskForm):
    email = StringField('Электронная почта', validators=[Email('Неправильный электронный адрес'),DataRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    checkbox = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')







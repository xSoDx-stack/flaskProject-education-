from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired

class LogIn(FlaskForm):
    email = StringField('Адрес', validators=[Email(), DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    checkbox = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')




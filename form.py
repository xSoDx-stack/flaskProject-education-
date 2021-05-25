from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField, BooleanField
from wtforms.validators import Email, InputRequired, DataRequired, EqualTo

class LogIn(FlaskForm):
    email = StringField('Электронная почта', validators=[Email('Неправильный электронный адрес'),DataRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    checkbox = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Registr(FlaskForm):
   email = StringField('Введите действующую электронную почту', validators=[Email('Неправильный электронный адрес'),DataRequired()])
   name = StringField('Введите ваше имя', validators=[InputRequired()])
   surname = StringField('Введите вашу фамилию', validators=[InputRequired()])
   password = PasswordField('Новый пароль', validators=[InputRequired(), EqualTo('password2', 'Пароли не совпадают')])
   password2 = PasswordField('Повторите пароль', validators=[InputRequired()])
   submit = SubmitField('Войти')






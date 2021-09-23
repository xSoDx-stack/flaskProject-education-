from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField, BooleanField
from wtforms.validators import Email, InputRequired, DataRequired, EqualTo



class LogIn(FlaskForm):
    email = StringField('Электронная почта', validators=[Email('Неправильно введена почта или пароль'),DataRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    # checkbox = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Registr(FlaskForm):
   email = StringField('Введите действующую электронную почту', validators=[Email('Неверная запись адреса электронной почты'),DataRequired()])
   name = StringField('Введите ваше имя', validators=[InputRequired()])
   surname = StringField('Введите вашу фамилию', validators=[InputRequired()])
   password = PasswordField('Придумайте пароль', validators=[InputRequired()])
   password2 = PasswordField('Повторите пароль', validators=[InputRequired(), EqualTo('password', 'Пароли не совпадают')])
   submit = SubmitField('Регистрация')
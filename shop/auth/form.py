from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, InputRequired, DataRequired, EqualTo


class LogIn(FlaskForm):
    email = StringField('Электронная почта', validators=[Email('Неверно введена почта или пароль'), DataRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    recaptcha = RecaptchaField('Подтвердите что вы не робот')
    submit = SubmitField('Войти')


class Registr(FlaskForm):
    email = StringField('Введите действующую электронную почту',
                        validators=[Email('Неверная запись адреса электронной почты'), DataRequired()])
    name = StringField('Введите ваше имя', validators=[InputRequired()])
    surname = StringField('Введите вашу фамилию', validators=[InputRequired()])
    password = PasswordField('Придумайте пароль', validators=[InputRequired()])
    password2 = PasswordField('Повторите пароль',
                              validators=[InputRequired(), EqualTo('password', 'Пароли не совпадают')])
    recaptcha = RecaptchaField('Подтвердите что вы не робот')
    submit = SubmitField('Регистрация')


class RequestResetPassword(FlaskForm):
    email = StringField('Введите ваш почтовый ящик для сброса пароля',
                        validators=[Email('Пользователь с данной почтой не найден'), DataRequired()])
    recaptcha = RecaptchaField('Подтвердите что вы не робот')
    submit = SubmitField('Востановить доступ')


class ResetPassword(FlaskForm):
    password = PasswordField('Придумайте новый пароль', validators=[InputRequired()])
    password2 = PasswordField('Повторите пароль',
                              validators=[InputRequired(), EqualTo('password', 'Пароли не совпадают')])
    submit = SubmitField('Сменить пароль')

from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, InputRequired, DataRequired, EqualTo, Length
from flask_security import ConfirmRegisterForm

class Registr(ConfirmRegisterForm):
    email = StringField('Введите действующую электронную почту',
                        validators=[Email('Неверная запись адреса электронной почты'), DataRequired()])
    username = StringField('Введите ваше имя', validators=[InputRequired('Это поле обязательно к заполнения')])
    surname = StringField('Введите вашу фамилию', validators=[InputRequired()])
    password = PasswordField('Придумайте пароль',
                             validators=[InputRequired(), DataRequired(), Length(min=8, message="Пароль должен содержать не менее %(min)d символов ")])
    password_confirm = PasswordField('Повторите пароль',
                              validators=[InputRequired(), EqualTo('password', 'Пароли не совпадают')])
    recaptcha = RecaptchaField('Подтвердите что вы не робот', validators=[Recaptcha("Вы не подтвердили что вы человек")])
    submit = SubmitField('Регистрация')


class LogIn(FlaskForm):
    email = StringField('Электронная почта', validators=[Email('Неверно введена почта или пароль'), DataRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    recaptcha = RecaptchaField('Подтвердите что вы не робот')
    submit = SubmitField('Войти')


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

from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Email, InputRequired, DataRequired, EqualTo, Length


class LogInForm(FlaskForm):
    email = StringField("Электронная почта", validators=[Email("Неверно введена почта или пароль",
                                                               check_deliverability=True), DataRequired()])
    password = PasswordField("Пароль", validators=[InputRequired()])
    recaptcha = RecaptchaField("Подтвердите что вы не робот",
                               validators=[Recaptcha("вы не подтвердили что вы не робот")])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class RegistrForm(FlaskForm):
    email = StringField("Введите действующую электронную почту",
                        validators=[Email("Неверная запись адреса электронной почты"), DataRequired()])
    name = StringField("Введите ваше имя", validators=[InputRequired()])
    surname = StringField("Введите вашу фамилию", validators=[InputRequired()])
    password = PasswordField("Придумайте пароль", validators=[InputRequired(), Length(8, 64, "Длина пароля должна быть "
                                                                                             "не менее 8 символов")])
    confirm_password = PasswordField("Повторите пароль",
                                     validators=[InputRequired(), EqualTo('password', "Пароли не совпадают")])
    recaptcha = RecaptchaField("Подтвердите что вы не робот",
                               validators=[Recaptcha("вы не подтвердили что вы не робот")])
    submit = SubmitField("Регистрация")


class RequestResetPasswordForm(FlaskForm):
    email = StringField("Введите ваш почтовый ящик для сброса пароля",
                        validators=[Email("Пользователь с данной почтой не найден"), DataRequired()])
    recaptcha = RecaptchaField("Подтвердите что вы не робот",
                               validators=[Recaptcha("вы не подтвердили что вы не робот")])
    submit = SubmitField("Востановить доступ")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Введите новый пароль",
                             validators=[InputRequired(), Length(8, 64, "Длина пароля должна быть не менее 8 символов")])
    confirm_password = PasswordField('Повторите пароль',
                                     validators=[InputRequired(), EqualTo('password', "Пароли не совпадают"),
                                                 Length(8, 64, "Длина пароля должна быть не менее 8 символов")])
    submit = SubmitField("Сменить пароль")

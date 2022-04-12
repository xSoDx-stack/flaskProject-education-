from flask import render_template
from flask_mail import Message
from shop import mail
from os import environ
from shop.models import User
from shop import login_manager


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    send_email(subject='Запрос на сброс вашего пароля',
               sender=environ.get('MAIL_USERNAME'),
               recipients=[user.email],
               text_body=render_template('auth/info_message/info_pass_res.html'),
               html_body=render_template('email/send_user_mail_reset_pas.html',
                                         name=user.name, token=user.get_generated_token()))


def user_activate_account(user):
    send_email(subject='Запрос на активацию вашего аккаунта',
               sender=environ.get('MAIL_USERNAME'),
               recipients=[user.email],
               text_body=render_template('auth/info_message/info_activate_account.html'),
               html_body=render_template('email/send_user_mail_activate.html',
                                         name=user.name, token=user.get_generated_token()))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

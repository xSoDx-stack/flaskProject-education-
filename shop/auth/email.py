from flask import render_template
from flask_mail import Message
from shop import mail
from os import environ


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(_mail):
    token = _mail.get_generated_token()
    send_email(subject='Запрос на сброс вашего пароля',
               sender=environ.get('MAIL_USERNAME'),
               recipients=[_mail.email],
               text_body=render_template('auth/info_message/info_pass_res.html'),
               html_body=render_template('email/send_user_mail_reset_pas.html',
                                         name=_mail.name, token=token))


def user_activate_account(_mail):
    token = _mail.get_generated_token()
    send_email(subject='Запрос на активацию вашего аккаунта',
               sender=environ.get('MAIL_USERNAME'),
               recipients=[_mail.email],
               text_body=render_template('auth/info_message/info_activate_account.html'),
               html_body=render_template('email/send_user_mail_activate.html',
                                         name=_mail.name, token=token))

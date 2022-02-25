from flask import render_template
from flask_mail import Message
from shop import mail
from os import environ


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(mail):
    token = mail.get_reset_password_token()
    send_email(subject='Запрос на сброс вашего пароля',
               sender=environ.get('MAIL_USERNAME'),
               recipients=[mail.email],
               text_body=render_template('auth/info_pass_res.html'),
               html_body=render_template('email/send_user_mail.html',
                                         name=mail.name, token=token))

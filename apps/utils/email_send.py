#!/usr/bin/python3.6
#-*-coding:utf-8-*-
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from OnlineCourse.settings import EMAIL_FROM

def random_string(randomlength=8):
    str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def send_register_email(e_mail, send_type="register"):
    rendom_code = random_string(16)

    emailRecord = EmailVerifyRecord()
    emailRecord.email = e_mail
    emailRecord.code= rendom_code
    emailRecord.send_type = send_type
    emailRecord.save()

    email_title = "Lzb Online Course Register Testing Mail"
    email_body = "Click here http://127.0.0.1:8000/active/{0}".format(rendom_code)

    if send_type == "register":
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [e_mail])
        if send_status:
            pass

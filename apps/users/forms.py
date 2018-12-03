#!/usr/bin/python3.6
#-*-coding:utf-8-*-

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.CharField(required=True, error_messages={"required": "邮箱格式不正确"})

    password = forms.CharField(required=True, min_length=6, error_messages={"min_length": "密码长度必须大于6"})
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.CharField(required=True, error_messages={"required": "邮箱格式不正确"})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})
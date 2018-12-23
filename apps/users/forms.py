#!/usr/bin/python3.6
#-*-coding:utf-8-*-

import re
import datetime
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile, EmailVerifyRecord


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


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, error_messages={"min_length": "密码长度必须大于6"})
    password2 = forms.CharField(required=True, min_length=6)


class ModifyUserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile

        fields = ['nick_name', 'birthday', 'gender', 'mobile', 'address']

    def clean_mobile(self):
        """
        check mobile is valid
        """
        mobile = self.cleaned_data['mobile']
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        p = re.compile(phone_pat)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码不合法", code="mobile_invalid")

    def clean_birthday(self):
        # check birthday is valid
        birthday = self.cleaned_data['birthday']
        today = datetime.date.today()
        delta = today - birthday
        if delta.days/365 >= 16:
            return birthday
        else:
            raise forms.ValidationError(u"用户的年龄必须大于16岁", code="birthday_invalid")


class UpdateEmailForm(forms.ModelForm):
    class Meta:
        model = UserProfile

        fields = ['email']


class EmailVerifyCodeForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyRecord
        fields = '__all__'


class UploadAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

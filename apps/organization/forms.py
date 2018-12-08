# -*- coding: utf-8 -*-

import re

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        check mobile is valid
        :return:
        """
        mobile = self.cleaned_data['mobile']
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        p = re.compile(phone_pat)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码不合法", code="mobile_invalid")

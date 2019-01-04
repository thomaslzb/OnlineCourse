# -*- coding: utf-8 -*-
from django.urls import path

from .views import UserInfoView, UserMyCourseView, UserMessageView, UserMyFavoriteView, UploadAvatarView
from .views import UpdateUserPasswordView, SendVerifyCodeView, UpdateEmailView

"""
users url
"""
app_name = "users"

urlpatterns = [
    # user information
    path('my-info/', UserInfoView.as_view(), name="my_info"),

    # user avatar
    path('upload/avatar/', UploadAvatarView.as_view(), name="upload_avatar"),

    # user update password
    path('update/password/', UpdateUserPasswordView.as_view(), name="update_password"),

    # user update email
    path('send_email/verify/', SendVerifyCodeView.as_view(), name="send_mail_for_verify"),
    path('update/email/', UpdateEmailView.as_view(), name="update_mail"),

    # My favorite courses
    path('my-courses/', UserMyCourseView.as_view(), name="my_courses"),

    # My favorite org
    path('my-favorites/<fav_item>/', UserMyFavoriteView.as_view(), name="my_favorites"),

    # My Messages
    path('my-messages/', UserMessageView.as_view(), name="my_messages"),
]

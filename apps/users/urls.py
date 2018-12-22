# -*- coding: utf-8 -*-
from django.urls import path

from .views import UserInfoView, UserMyCourseView, UserMessageView, UserMyFavoriteView, UploadAvatarView
from .views import UpdateUserPasswordView

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

    path('my-courses/', UserMyCourseView.as_view(), name="my_courses"),
    path('my-favorites/', UserMyFavoriteView.as_view(), name="my_favorites"),
    path('my-messages/', UserMessageView.as_view(), name="my_Messages"),
]

# -*- coding: utf-8 -*-
from django.urls import path

from .views import UserInfoView, UserMyCourseView, UserMessageView, UserMyFavoriteView, UploadAvatarView

"""
users url
"""
app_name = "users"

urlpatterns = [
    # user information
    path('my-info/', UserInfoView.as_view(), name="my_info"),

    # user avatar
    path('upload/avatar/', UploadAvatarView.as_view(), name="upload_avatar"),

    path('my-courses/', UserMyCourseView.as_view(), name="my_courses"),
    path('my-favorites/', UserMyFavoriteView.as_view(), name="my_favorites"),
    path('my-messages/', UserMessageView.as_view(), name="my_Messages"),
]

# -*- coding: utf-8 -*-
from django.urls import path

from .views import UserInfoView, UserMyCourseView, UserMessageView, UserMyFavoriteView

"""
users url
"""
app_name = "users"

urlpatterns = [
    path('my-info/', UserInfoView.as_view(), name="my_info"),
    path('my-courses/', UserMyCourseView.as_view(), name="my_courses"),
    path('my-favorites/', UserMyFavoriteView.as_view(), name="my_favorites"),
    path('my-messages/', UserMessageView.as_view(), name="my_Messages"),
]

# -*- coding: utf-8 -*-
from django.urls import path

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView

"""
Course url
"""

app_name = "courses"

# course list
urlpatterns = [
    path('list/', CourseListView.as_view(), name="list"),
]

# course detail
urlpatterns += [
    path('detail/<course_id>/', CourseDetailView.as_view(), name='detail'),
    path('course_info/<course_id>/', CourseInfoView.as_view(), name='course_info'),
    path('course_comment/<course_id>/', CourseCommentView.as_view(), name='course_comment'),
    path('add_comment/<course_id>/', AddCommentView.as_view(), name='add_comment'),
]



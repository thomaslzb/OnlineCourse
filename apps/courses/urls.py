# -*- coding: utf-8 -*-
from django.urls import path

from .views import CourseListView, CourseDetailView

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
    path('course_detail/<course_id>/', CourseDetailView.as_view(), name='course_detail'),
]


# courses detail
urlpatterns += [

]

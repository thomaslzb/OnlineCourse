# -*- coding: utf-8 -*-
from django.urls import path

from .views import OrgListView, UserAskView
from .views import OrgHomeView, OrgDetailCourseView, OrgDetailTeacherView, OrgDetailDescView, AddFavoriteView
from .views import TeacherListView, TeacherDetailView


"""
Organization url
"""

app_name = "organization"

# organization list
urlpatterns = [
    path('list/', OrgListView.as_view(), name="list"),
]

# user inquire
urlpatterns += [
    path('user_ask/', UserAskView.as_view(), name='user_ask'),
]

# org detail
urlpatterns += [
    path('org_home/<company_id>/', OrgHomeView.as_view(), name='org_home'),
    path('org_detail_course/<company_id>/', OrgDetailCourseView.as_view(), name='org_detail_course'),
    path('org_detail_teacher/<company_id>/', OrgDetailTeacherView.as_view(), name='org_detail_teacher'),
    path('org_detail_desc/<company_id>/', OrgDetailDescView.as_view(), name='org_detail_desc'),

    # user favorite or cancel favorite
    path('add_favorite/', AddFavoriteView.as_view(), name='add_favorite'),
]


# teacher list
urlpatterns += [
    path('teacher_list/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher_detail/<teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail'),
]

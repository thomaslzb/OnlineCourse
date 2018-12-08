# -*- coding: utf-8 -*-
from django.urls import path
from .views import OrgListView, UserAskView

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

# -*- coding: utf-8 -*-
import xadmin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, PasswordResetView

# Uncomment the next two lines to enable the admin:

# xadmin.autodiscover()
#
# # version模块自动注册需要版本控制的 Model
# from xadmin.plugins import xversion
# xversion.register_models()
# from django.contrib import admin


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('captcha/', include('captcha.urls')),
]

# index
urlpatterns += [
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
]

urlpatterns += [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    re_path(r'active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    path('forget_pwd/', ForgetPwdView.as_view(), name="forget_pwd"),
    re_path(r'password_reset/(?P<active_code>.*)/$', PasswordResetView.as_view(), name="password_reset"),
    # path('logout/', user_login, name="logout")
]

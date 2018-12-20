# -*- coding: utf-8 -*-
import xadmin
from django.urls import include, path
from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, PasswordResetView, ModifyPwdView
from organization.views import TeacherListView
from views import IndexView

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
    path('', IndexView.as_view(), name="index"),
]

"""
user url 
"""
urlpatterns += [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('active/<active_code>/', ActiveUserView.as_view(), name="user_active"),
    path('forget_pwd/', ForgetPwdView.as_view(), name="forget_pwd"),
    path('password_reset/<active_code>/', PasswordResetView.as_view(), name="password_reset"),
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),
    # path('logout/', user_login, name="logout")
]

"""
Organization url
"""
urlpatterns += [
    path('org/', include('organization.urls', namespace='org')),
]

"""
Course url
"""
urlpatterns += [
    path('course/', include('courses.urls', namespace='courses')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


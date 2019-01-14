# -*- coding: utf-8 -*-
import xadmin
from django.urls import include, path
from django.conf.urls import url, handler400, handler403, handler404, handler500

from django.conf import settings
from django.conf.urls.static import static, serve

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, PasswordResetView, ModifyPwdView, LogoutView

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
user operation
"""
urlpatterns += [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('active/<active_code>/', ActiveUserView.as_view(), name="user_active"),
    path('forget_pwd/', ForgetPwdView.as_view(), name="forget_pwd"),
    path('password_reset/<active_code>/', PasswordResetView.as_view(), name="password_reset"),
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),
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

"""
user center url 
"""
urlpatterns += [
    path('users/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    """
    定义图片的根目录
    """
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    """
    如果 DEBUG = False , 即在生产环境下
    """
    urlpatterns += [
        # path('media/', serve, {"document_root": settings.MEDIA_ROOT}),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    ]

"""
handle 404, 500, ,403
"""
handler400 = 'apps.users.views.bad_request'
handler403 = 'apps.users.views.permission_denied'
handler404 = 'apps.users.views.page_not_found'
handler500 = 'apps.users.views.server_error'

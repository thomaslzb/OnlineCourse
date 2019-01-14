# -*- coding: utf-8 -*-
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from pure_pagination import Paginator, PageNotAnInteger
from django.template import RequestContext

from django.shortcuts import render
from django.shortcuts import render_to_response

from users.models import UserProfile, EmailVerifyRecord
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course

from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, ModifyUserInfoForm
from users.forms import UploadAvatarForm, UpdateEmailForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    """
    user logout
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    """
    user login
    """
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_from = LoginForm(request.POST)
        if login_from.is_valid():
            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")

            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": "用户未激活!"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_form": login_from })


class RegisterView(View):
    """
    user register
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form":register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password","")

            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户名已经存在"})

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.has_read = False
            user_message.message = "欢迎注册在线课程网， 希望你能够在网站上找到你需要的课程或老师！"
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, "register_mail_success.html")
        else:
            return render(request, "register.html", {"register_form":register_form})


class ActiveUserView(View):
    """
    Active user
    """
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            render(request, "active_failure.html")

        return render(request, "login.html")


class ForgetPwdView(View):
    """
    Forget password
    """
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetPwd_form": forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get("email", "")
            if not (UserProfile.objects.filter(email=email)):
                return render(request, "forgetpwd.html", {"forgetPwd_form": forgetpwd_form, "msg": "用户邮箱不存在"})

            # send a new mail for reset password

            send_register_email(email, "forget")
            return render(request, "send_resetPwd_success.html")
        else:
            return render(request, "forgetpwd.html", {"forgetPwd_form": forgetpwd_form})


class PasswordResetView(View):
    """
    Password Reset
    """
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
            return render(request, "password_reset.html", {'email': email})
        else:
            return render(request, "active_failure.html")


class ModifyPwdView(View):
    """
    Modify user's password
    """
    def post(self, request):
        modifypwdform = ModifyPwdForm(request.POST)
        email = request.POST.get("email", "")
        if modifypwdform.is_valid():
            pass1 = request.POST.get("password1", "")
            pass2 = request.POST.get("password2", "")
            if pass1 != pass2:
                return render(request, "password_reset.html", {"modifypwd_form": modifypwdform,
                                                               "email": email, "msg": "两次输入的密码不一致"})

            user_profile = UserProfile.objects.get(email=email)
            if user_profile:
                user_profile.password = make_password(pass1)
                user_profile.save()
                return render(request, "modifypwd_success.html")
        else:
            return render(request, "password_reset.html", {"modifypwd_form": modifypwdform, "email": email})


class UserInfoView(LoginRequiredMixin, View):
    """
    User info
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        """
        user modify information
        """
        user_form = ModifyUserInfoForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse('{"status": "success", "msg": "个人信息修改成功" }', content_type='application/json')
        return HttpResponse(json.dumps(user_form.errors), content_type='application/json')


class UploadAvatarView(LoginRequiredMixin, View):
    """
     User update Avatar
    """
    def post(self, request):
        upload_avatar = UploadAvatarForm(request.POST, request.FILES, instance=request.user)
        if upload_avatar:
            upload_avatar.save()
            return HttpResponse('{"status": "success", "msg": "用户头像修改成功" }', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "用户头像修改失败" }', content_type='application/json')


class UpdateUserPasswordView(LoginRequiredMixin, View):
    """
    User update password
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pass1 = request.POST.get("password1", "")
            pass2 = request.POST.get("password2", "")
            if pass1 != pass2:
                return HttpResponse('{"status": "fail", "msg": "两次输入的密码不一致" }', content_type='application/json')
            else:
                user = request.user
                user.password = make_password(pass1)
                user.save()
                return HttpResponse('{"status": "success", "msg": "用户密码更新成功" }', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendVerifyCodeView(LoginRequiredMixin, View):
    """
    send a email for verification code
    """
    def get(self, request):
        email = request.GET.get('email', '')
        if send_register_email(email, "update_email"):
            return HttpResponse('{"status": "success"', content_type='application/json')
        else:
            return HttpResponse('{"status": "failure"', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
     User update email
    """
    def post(self, request):
        verify_code = request.POST.get('code', '')
        email = request.POST.get('email', '')
        if verify_code != "" and email != "":
            user_form = UpdateEmailForm(request.POST, instance=request.user)
            # check verify code is valid
            email_record = EmailVerifyRecord.objects.get(code=verify_code, email=email, send_type="update_email")
            if email_record:
                user_form.save()
                return HttpResponse('{"status": "success"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "failure"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(UpdateEmailForm.errors), content_type='application/json')


class UserMyCourseView(LoginRequiredMixin, View):
    """
    Users Courses
    """
    def get(self, request):
        my_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {"my_courses": my_courses})


class UserMyFavoriteView(LoginRequiredMixin, View):
    """
    Users Favorites
    """
    def get(self, request, fav_item):
        if fav_item == "teachers":
            user_fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
            teacher_ids = [fav_teacher.fav_id for fav_teacher in user_fav_teachers]

            user_fav = Teacher.objects.filter(id__in=teacher_ids)
            return render(request, 'usercenter-fav-teacher.html', {"fav_item": fav_item,
                                                                   "user_fav": user_fav,
                                                                   })
        elif fav_item == "courses":
            user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
            user_course_ids = [fav_course.fav_id for fav_course in user_fav_courses]

            user_fav = Course.objects.filter(id__in=user_course_ids)
            return render(request, 'usercenter-fav-course.html', {"fav_item": fav_item,
                                                                  "user_fav": user_fav,
                                                                  })
        else:
            user_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
            user_org_ids = [user_org.fav_id for user_org in user_fav_orgs]

            user_fav = CourseOrg.objects.filter(id__in=user_org_ids)

            return render(request, 'usercenter-fav-org.html', {"fav_item": fav_item,
                                                               "user_fav": user_fav,
                                                               })


class UserMessageView(LoginRequiredMixin, View):
    """
    Users Message
    """
    def get(self, request):
        user_messages = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')

        # Clear this user's unread message
        user_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in user_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_messages, 8, request=request)
        p_messages = p.page(page)

        return render(request, 'usercenter-message.html', {"user_messages": p_messages,
                                                           })


def bad_request(request):
    """
    handle 400
    """
    context = RequestContext(request)
    err_code = 400
    response = render_to_response('404.html', {"code": err_code}, context)
    response.status_code = 400
    return response


def page_not_found(request):
    """
    handle 404
    """
    context = RequestContext(request)
    err_code = 404
    response = render_to_response('404.html', {"code": err_code}, context)
    response.status_code = 404
    return response


def server_error(request):
    """
    handle 500
    """
    context = RequestContext(request)
    err_code = 500
    response = render_to_response('500.html', {"code": err_code}, context)
    response.status_code = 500
    return response


def permission_denied(request):
    """
    handle 403
    """
    context = RequestContext(request)
    err_code = 403
    response = render_to_response('403.html', {"code": err_code}, context)
    response.status_code = 403
    return response


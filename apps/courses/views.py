from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource
from operation.models import UserFavorite, UserCourse, CourseComments
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    """
    课程的列表页面
    """
    def get(self, request):
        nav_course = True

        all_courses = Course.objects.all().order_by("-add_time")

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_courses = Course.objects.order_by("-click_nums")
            elif sort == "students":
                all_courses = Course.objects.order_by("-students")

        hot_courses = Course.objects.order_by("-click_nums")[:5]

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 9, request=request)
        p_courses = p.page(page)

        return render(request, "course-list.html", {"nav_course": nav_course,
                                                    "all_courses": p_courses,
                                                    "hot_courses": hot_courses,
                                                    "sort": sort,
                                                    })


class CourseDetailView(LoginRequiredMixin, View):
    """
    课程的详情页面
    """
    def get(self, request, course_id):
        nav_course = True
        course_detail = Course.objects.get(id=int(course_id))

        # 保存用户的课程点击数
        course_detail.click_nums += 1
        course_detail.save()

        if not course_detail:
            """
            无此课程
            """
            return render(request, "course-list.html", {"nav_course": nav_course,
                                                        })
        # 判断用户是否收藏此课程
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_detail.course_org.id), fav_type=2):
                has_fav_org = True

        # 提取相关课程
        tag = course_detail.tag
        if tag:
            relate_courses = Course.objects.filter(~Q(id=course_id), tag=tag)[:2]
        else:
            relate_courses = []

        return render(request, "course-detail.html", {"nav_course": nav_course,
                                                      "course_detail": course_detail,
                                                      "has_fav_course": has_fav_course,
                                                      "has_fav_org": has_fav_org,
                                                      "relate_courses": relate_courses,
                                                      })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程详情的章节及资源的下载
    """
    def get(self, request, course_id):
        nav_course = True
        course_detail = Course.objects.get(id=int(course_id))

        # 保存用户开始学习此课程的信息
        user_course = UserCourse.objects.filter(course=course_detail.id, user=request.user)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course_detail)
            user_course.save()

        # 查询学过该课的同学的课程
        user_courses = UserCourse.objects.filter(course=course_detail)
        user_ids = [user_course.user.id for user_course in user_courses]

        # 查询其它用户学过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出所有相关课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_coursers = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        # 取得课程的资源信息
        course_rescourses = CourseResource.objects.filter(course=course_detail)

        return render(request, "course-video.html", {"course_detail": course_detail,
                                                     "nav_course": nav_course,
                                                     "course_rescourses": course_rescourses,
                                                     "relate_coursers": relate_coursers,
                                                     })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程详情的课程评论
    """
    def get(self, request, course_id):
        nav_course = True
        course_detail = Course.objects.get(id=int(course_id))

        course_comments = CourseComments.objects.filter(course=course_detail).order_by('-add_time')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(course_comments, 4, request=request)
        p_comments = p.page(page)

        # 保存用户开始学习此课程的信息
        user_course = UserCourse.objects.filter(course=course_detail.id, user=request.user)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course_detail)
            user_course.save()

        # 查询学过该课的同学的课程
        user_courses = UserCourse.objects.filter(course=course_detail)
        user_ids = [user_course.user.id for user_course in user_courses]

        # 查询其它用户学过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出所有相关课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_coursers = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        # 取得课程的资源信息
        course_rescourses = CourseResource.objects.filter(course=course_detail)

        return render(request, "course-comment.html", {"course_detail": course_detail,
                                                       "nav_course": nav_course,
                                                       "course_rescourses": course_rescourses,
                                                       "relate_coursers": relate_coursers,
                                                       "course_comments": p_comments,
                                                       })


class AddCommentView(LoginRequiredMixin, View):
    """
    增加课程评论
    """
    def post(self, request, course_id):
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status": "success", "msg": "添加成功" }', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败" }', content_type='application/json')

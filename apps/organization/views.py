# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger


from .models import CourseOrg, CityDict, Teacher
from operation.models import UserFavorite
from .forms import UserAskForm


class OrgListView(View):
    """
        课程机构列表显示
    """
    def get(self, request):
        # All Organization
        nav_org = True
        all_orgs = CourseOrg.objects.all()

        # All City
        all_cities = CityDict.objects.all()

        # filter city
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city=city_id)

        # filter category
        category_code = request.GET.get('ct', "")
        if category_code:
            all_orgs = all_orgs.filter(category=category_code)

        # sort students and courses
        sort = request.GET.get('sort', "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")
        else:
            all_orgs = all_orgs.order_by("-add_time")

        all_orgs_nums = all_orgs.count()

        # Organization Rate
        hot_orgs = all_orgs.order_by("-click_nums")[:5]

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {"all_orgs": orgs,
                                                 "all_cities": all_cities,
                                                 "all_orgs_nums": all_orgs_nums,
                                                 "city_id": city_id,
                                                 "ct": category_code,
                                                 "sort": sort,
                                                 "hot_orgs": hot_orgs,
                                                 "nav_org": nav_org,
                                                 })


class UserAskView(View):
    """
    user inquire
    """
    def post(self, request):
        userask = UserAskForm(request.POST)
        if userask.is_valid():
            userask = userask.save(commit=True)
            # 注意下一句中的单引号和双引号，如果写反了，在html中的ajax种会出现错误
            # parsererror: SyntaxError: Unexpected token ' in JSON at position 1
            return HttpResponse('{"status": "success"}',  content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    organization home detail
    """
    def get(self, request, company_id):
        nav_org = True
        home_page = True

        the_org = CourseOrg.objects.get(id=int(company_id))

        if not the_org:
            return render(request, 'index.html', {})

        # 判断用户是否已经收藏此机构
        has_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(company_id), fav_type=2):
                has_favorite = True

        all_course = the_org.course_set.all()[:3]
        all_teacher = the_org.teacher_set.all()[:3]
        return render(request, 'org-detail-homepage.html',
                      {"the_org": the_org,
                       "all_course": all_course,
                       "all_teacher": all_teacher,
                       "company_id": company_id,
                       "home_page": home_page,
                       "nav_org": nav_org,
                       "has_favorite": has_favorite,
                       })


class OrgDetailCourseView(View):
    """
    organization course detail
    """
    def get(self, request, company_id):
        course_page = True
        the_org = CourseOrg.objects.get(id=int(company_id))
        if not the_org:
            return render(request, 'index.html', {})

        # 判断用户是否已经收藏此机构
        has_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(company_id), fav_type=2):
                has_favorite = True

        all_course = the_org.course_set.all()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 12, request=request)
        p_courses = p.page(page)

        return render(request, 'org-detail-course.html',
                      {"the_org": the_org,
                       "all_courses": p_courses,
                       "company_id": company_id,
                       "course_page": course_page,
                       "has_favorite": has_favorite,
                       })


class OrgDetailTeacherView(View):
    """
    organization teacher detail
    """
    def get(self, request, company_id):
        teacher_page = True
        the_org = CourseOrg.objects.get(id=int(company_id))
        if not the_org:
            return render(request, 'index.html', {})

        # 判断用户是否已经收藏此机构
        has_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(company_id), fav_type=2):
                has_favorite = True

        all_teachers = the_org.teacher_set.all()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 8, request=request)
        p_teachers = p.page(page)

        return render(request, 'org-detail-teachers.html',
                      {"the_org": the_org,
                       "all_teachers": p_teachers,
                       "company_id": company_id,
                       "teacher_page": teacher_page,
                       "has_favorite": has_favorite
                       })


class OrgDetailDescView(View):
    """
    organization desc detail
    """
    def get(self, request, company_id):
        desc_page = True
        the_org = CourseOrg.objects.get(id=int(company_id))
        if not the_org:
            return render(request, 'index.html', {})

        # 判断用户是否已经收藏此机构
        has_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(company_id), fav_type=2):
                has_favorite = True

        return render(request, 'org-detail-desc.html',
                      {"the_org": the_org,
                       "company_id": company_id,
                       "desc_page": desc_page,
                       "has_favorite": has_favorite,
                       })


class AddFavoriteView(View):
    """
    User add favorite or cancel favorate
    """
    def post(self, request):
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get("fav_type", 0)

        if not request.user.is_authenticated:
            """
            user isn't login in
            """
            return HttpResponse('{"status": "fail", "msg": "用户未登录" }', content_type='application/json')

        if int(fav_type) == 0 or int(fav_id) == 0:
            return HttpResponse('{"status": "fail", "msg": "收藏出错" }', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            """
            cancel user favorite
            """
            exist_record.delete()
            return HttpResponse('{"status": "success", "msg": "收藏" }', content_type='application/json')
        else:
            user_favorite = UserFavorite()
            user_favorite.user = request.user
            user_favorite.fav_id = int(fav_id)
            user_favorite.fav_type = int(fav_type)
            user_favorite.save()
            return HttpResponse('{"status": "success", "msg": "已收藏" }', content_type='application/json')


class TeacherListView(View):
    """
    教师列表页
    """
    def get(self, request):
        nav_teacher = True

        # 全部教师
        # sort students and courses
        sort = request.GET.get('sort', "")
        all_teachers = Teacher.objects.all().order_by('add_time')
        if sort == "hot":
            all_teachers = Teacher.objects.all().order_by('-click_nums')

        all_teachers_nums = all_teachers.count()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 8, request=request)
        p_teachers = p.page(page)

        # 教师排行榜-根据点击数
        top_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        return render(request, "teachers-list.html", {"nav_teacher": nav_teacher,
                                                      "all_teachers": p_teachers,
                                                      "all_teachers_nums": all_teachers_nums,
                                                      "top_teachers": top_teachers,
                                                      "sort": sort,
                                                      })


class TeacherDetailView(View):
    """
    教师详情页
    """
    def get(self, request, teacher_id):
        nav_teacher = True

        # 教师排行
        top_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        # 取得教师的资料
        teacher = Teacher.objects.get(id=teacher_id)

        # 取得教师的课程

        return render(request, "teacher-detail.html", {"nav_teacher": nav_teacher,
                                                       "top_teachers": top_teachers,
                                                       "teacher": teacher,

                                                       })

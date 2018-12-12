from django.shortcuts import render
from django.views import View

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course


class CourseListView(View):
    def get(self, request):
        nav_course = True

        sort = request.GET.get('sort', "")
        sort_students = False
        sort_all = False
        sort_hot = False
        if sort == "hot":
            sort_hot = True
            all_courses = Course.objects.order_by("-fav_nums")
        elif sort == "students":
            sort_students = True
            all_courses = Course.objects.order_by("-students")
        else:
            sort_all = True
            all_courses = Course.objects.order_by("-add_time")

        hot_courses = Course.objects.order_by("-fav_nums")[:3]

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
                                                    "sort_hot": sort_hot,
                                                    "sort_students": sort_students,
                                                    "sort_all": sort_all,
                                                    })


class CourseDetailView(View):
    def get(self, request, course_id):
        nav_course = True

        return render(request, "course-detail.html", {"nav_course": nav_course,
                                                      "course_id": course_id
                                                    })

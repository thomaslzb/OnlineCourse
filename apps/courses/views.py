from django.shortcuts import render
from django.views import View

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course


class CourseListView(View):
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


class CourseDetailView(View):
    def get(self, request, course_id):
        nav_course = True
        course_detail = Course.objects.get(id=int(course_id))
        if not course_detail:
            """
            无此课程
            """
            return render(request, "course-list.html", {"nav_course": nav_course,
                                                        })
        # users = Course.get_learn_users()

        return render(request, "course-detail.html", {"nav_course": nav_course,
                                                      "course_detail": course_detail,

                                                      })

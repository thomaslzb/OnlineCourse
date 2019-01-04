# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import View

from courses.models import Course
from organization.models import CourseOrg
from users.models import Banner


class IndexView(View):
    """
    Course Online Home Page
    """
    def get(self, request):
        # Banner
        all_banners = Banner.objects.order_by("-index")[:5]

        # Get all couurses
        all_course_banners = Course.objects.filter(is_banner=True)[:3]
        all_courses = Course.objects.order_by('-add_time')[:6]

        all_orgs = CourseOrg.objects.order_by('-click_nums')[:15]
        return render(request, 'index.html', {"all_courses": all_courses,
                                              "all_course_banners": all_course_banners,
                                              "all_orgs": all_orgs,
                                              "all_banners": all_banners,
                                              })

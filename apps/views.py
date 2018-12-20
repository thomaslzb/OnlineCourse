# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import View

from courses.models import Course
from organization.models import CourseOrg


class IndexView(View):
    def get(self, request):
        all_courses = Course.objects.order_by('-add_time')[:8]
        all_orgs = CourseOrg.objects.order_by('-click_nums')[:15]
        return render(request, 'index.html', {"all_courses": all_courses,
                                              "all_orgs": all_orgs,
                                              })

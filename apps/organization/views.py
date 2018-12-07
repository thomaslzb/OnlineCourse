# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict

class OrgListView(View):
    """
        课程机构列表显示
    """
    def get(self, request):
        # All Organization
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
                                                 })

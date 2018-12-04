# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View


class OrgListView(View):
    def get(self, request):
        return render(request, 'org-list.html')

#!/usr/bin/python3.6
#-*-coding:utf-8-*- 

import xadmin

from xadmin import views

from .models import EmailVerifyRecord
from .models import Banner


class GlobalSettings(object):
    site_title = "Course System Management"
    site_footer = "Lzb Company"
    menu_style = "accordion"



class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type','send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type','send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url','index', 'add_time']
    search_fields = ['title']
    list_filter =  ['title', 'image', 'url','index', 'add_time']


# register xadmin
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
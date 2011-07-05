#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/05]

from sales.models import Sales, Date, App, Country, Review, Admob
from django.contrib import admin

import datetime

class SalesAdmin(admin.ModelAdmin):
    list_display = ('app', 'date', 'units', 'country', 'proceeds', 'currency',  'category')
    list_filter = ('app', 'category')
    date_hierarchy = 'date'

class AdmobAdmin(admin.ModelAdmin):
    list_display = ('app', 'date', 'requests', 'clicks', 'revenue')
    list_filter = ('app', 'date')
    date_hierarchy = 'date'
    
    
class DateAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'account', 'populated', 'created')
    list_filter = ('date',)
    search_filters = ('date',)
    ordering = ('-date',)
    date_hierarchy = 'date'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('app', 'country', 'stars',  'ignore', 'reviewer', 'version','title', 'content')
    ordering = ('-version', '-date', '-ignore')
    list_filter = ('app', )
    actions = ['mark_ignore']
    
    def mark_ignore(self, request, queryset):
        queryset.update(ignore=True)
    mark_ignore.short_description = "Mark selected reviews as ignored"


admin.site.register(Sales, SalesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Date, DateAdmin)
admin.site.register(Country)
admin.site.register(App)
admin.site.register(Admob, AdmobAdmin)



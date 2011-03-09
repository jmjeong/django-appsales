#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/05]

from sales.models import Sales, Date, App, Country, Review
from django.contrib import admin

import datetime

class SalesAdmin(admin.ModelAdmin):
    list_display = ('app', 'date', 'units', 'country', 'proceeds', 'currency',  'category')
    list_filter = ('app', 'category')
    date_hierarchy = 'date'
    
class DateAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'account', 'populated', 'created')
    list_filter = ('date',)
    search_filters = ('date',)
    ordering = ('-date',)
    date_hierarchy = 'date'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('app', 'country', 'stars',  'reviewer', 'version','title', 'content')
    ordering = ('-version', '-date')
    list_filter = ('app', )
    

admin.site.register(Sales, SalesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Date, DateAdmin)
admin.site.register(Country)
admin.site.register(App)


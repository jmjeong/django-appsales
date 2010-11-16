#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/03]

# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.shortcuts import render_to_response

from django.contrib.auth import logout
from django.db.models import Avg, Sum

from sales.models import *

import datetime
from itertools import groupby

@csrf_protect
def main_page(request):
    return main_sort_page(request, 'name')

@login_required
def main_sort_page(request, sort):

    dateSet = Date.objects.all().order_by('-date')
    
    try:
        page = int(request.GET['page'])
    except:
        page = 1

    try:
        date = dateSet[page-1]
    except:
        if len(dateSet) > 0:
            raise Http404
        
    resultSet = []
    countrySet = []

    apps = App.objects.all()
    
    for a in apps:
        result = {}
        result['name'] = a.name
        result['appid'] = a.id
        
        ss = Sales.objects.filter(app=a, date=date.date).values('category').annotate(Sum('units'))
        for s in ss:
            result[s['category']] = s['units__sum']
        resultSet.append(result)

    # Sort resultSet by Sort category
    resultSet.sort(reverse=True,key=lambda r:r.has_key(sort) and r[sort] or 0)

    # generate statistic data
    summary = generate_summary(resultSet)
    
    if resultSet:
        if sort == 'name':
            cs = Sales.objects.filter(date=date.date).values('country').annotate(Sum('units')).order_by('-units__sum')[:len(apps)]
        else:
            cs = Sales.objects.filter(date=date.date, category=sort).values('country').annotate(Sum('units')).order_by('-units__sum')[:len(apps)]
            
        # Convert country pk into country name
        countrySet = map(
            lambda k: {'country':Country.objects.get(pk=k['country']).name, 'units__sum': k['units__sum']},
            cs)
        dateStr = date.date.strftime('%Y/%m/%d %a')
    else:
        dateStr = None

    var = RequestContext(request, {
        'dateStr' : dateStr,
        'dateSet' : dateSet,
        'resultSet' : resultSet,
        'summary': summary,
        'countrySet' : countrySet,
                           
        'page' : page,
        })
    return render_to_response('main_page.html', var)


def app_page(request, appid):
    return app_sort_page(request, appid, 'date')

@login_required
def app_sort_page(request, appid, sort='date'):
    
    try:
        appName = App.objects.get(pk=appid).name
    except:
        raise Http404

    ITEMS_PER_PAGE = 14
    
    sales = Sales.objects.filter(app=appid).values('date','category').annotate(Sum('units'))
    
    resultSet = []
    countrySet = []
    
    for date, fs in groupby(sorted(sales, key=lambda r:r['date'], reverse=True),
                           key=lambda r:r['date']):
        result = {}
        result['date'] = date.strftime('%Y/%m/%d %a')

        for f in fs:
            result[f['category']] = f['units__sum']

        resultSet.append(result)

    # Sort resultSet by Sort category
    resultSet.sort(reverse=True,key=lambda r:r.has_key(sort) and r[sort] or 0)

    if resultSet:
        if sort == 'date':
            cs = Sales.objects.filter(app=appid).values('country').annotate(Sum('units')).order_by('-units__sum')[:ITEMS_PER_PAGE]
        else:
            cs = Sales.objects.filter(app=appid, category=sort).values('country').annotate(Sum('units')).order_by('-units__sum')[:ITEMS_PER_PAGE]
            
        # Convert country pk into country name
        countrySet = map(
            lambda k: {'country':Country.objects.get(pk=k['country']).name, 'units__sum': k['units__sum']},
            cs)


    # Paginator
    try:
        page = int(request.GET['page'])
    except:
        page = 1

    paginator = Paginator(resultSet, ITEMS_PER_PAGE)

    try:
        subResultSet = paginator.page(page)
    except:
        page = max(paginator.page_range)
        subResultSet = paginator.page(page)

    # generate statistic data
    summary = generate_summary(resultSet)
    subsummary = generate_summary(subResultSet.object_list)

    var = RequestContext(request, {
        'appName': appName,
        'appid': appid,
        'resultSet' : resultSet,
        'countrySet' : countrySet,
        'subsummary': subsummary,
        'summary':summary,

        'ITEMS_PER_PAGE' : ITEMS_PER_PAGE,
        'page' : page,
        })
    return render_to_response('app_page.html', var)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def generate_summary(resultSet):
    summary = {}
    
    summary['FR'] = sum([f['FR'] for f in resultSet if f.has_key('FR')])
    summary['UP'] = sum([f['UP'] for f in resultSet if f.has_key('UP')])
    summary['PA'] = sum([f['PA'] for f in resultSet if f.has_key('PA')])
    summary['IA'] = sum([f['IA'] for f in resultSet if f.has_key('IA')])
    
    return summary

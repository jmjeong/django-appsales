#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Jaemok Jeong(jmjeong@gmail.com)
#
# [2011/03/15]

from django_extensions.management.jobs import BaseJob, HourlyJob
from sales.models import App, Date, Country, Review, Sales, Admob
from settings import *
import datetime

class Job(BaseJob):
    help = "Download sales data from Admob"

    def execute(self):
        from utils.admobapi import AdmobApi

        client_key = ADMOB_INFO['client_key']
        email = ADMOB_INFO['email']
        passwd = ADMOB_INFO['passwd']

        admobapi = AdmobApi(client_key)
        token = admobapi.login(email, passwd)

        today = datetime.datetime.now()
        # start_date = datetime.date(2009,1,1)
        start_date = today + datetime.timedelta(days=-8)
        end_date = today + datetime.timedelta(days=0)

        result = admobapi.search(token)
        for i in result:
            appname = i['name']

            try:
                app_id = App.objects.get(name=appname)
            except App.DoesNotExist:
                continue
            
            data = admobapi.stats(token, id=i['id'],
                               start_date=start_date.strftime('%Y-%m-%d'),
                               end_date=end_date.strftime('%Y-%m-%d'))

            for j in data:
                # Update admob data even if it exists, because it is updated in realtime
                #
                try:
                    admob = Admob.objects.get(app = app_id, date=j['date'])
                except Admob.DoesNotExist:
                    if j['requests'] == 0: continue
                    print j
                    
                    admob = Admob()
                    admob.app = app_id
                    admob.date = j['date']

                admob.requests = j['requests']
                admob.overall_requests = j['overall_requests']
                admob.housead_requests = j['housead_requests']
                admob.interstitial_requests = j['interstitial_requests']
                admob.impressions = j['impressions']
                admob.cpc_impressions = j['cpc_impressions']
                admob.cpm_impressions = j['cpm_impressions']
                admob.exchange_impressions = j['exchange_impressions']
                admob.housead_impressions = j['housead_impressions']
                admob.interstitial_impressions = j['interstitial_impressions']
                admob.fill_rate = j['fill_rate']
                admob.housead_fill_rate = j['housead_fill_rate']
                admob.overall_fill_rate = j['overall_fill_rate']
                admob.clicks = j['clicks']
                admob.housead_clicks = j['housead_clicks']
                admob.ctr = j['ctr']
                admob.housead_ctr = j['housead_ctr']
                admob.ecpm = j['ecpm']
                admob.revenue = j['revenue']
                admob.cpc_revenue = j['cpc_revenue']
                admob.cpm_revenue = j['cpm_revenue']
                admob.exchange_downloads = j['exchange_downloads']

                # print admob
                admob.save()
                    

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/03]

from django_extensions.management.jobs import BaseJob, HourlyJob
from sales.models import App, Date, Sales, Country
from settings import *

class Job(BaseJob):
    help = "Populate apple id field from data set"

    def check_done(self):
        if not App.objects.filter(appleid=None):
            return True
        else:
            return False

    def execute(self):
        import os
        import sys
        import csv

        print self.help

        for i in ACCOUNT_INFO:

            if (i['DATA_DIR'] != '' and not os.path.exists(i['DATA_DIR'])):
                os.makedirs(i['DATA_DIR'])

            filenames = [os.path.join(i['DATA_DIR'], f)
                         for f in os.listdir(i['DATA_DIR'])
                         if f.startswith(DAILY_SALES_PREFIX)]

            for f in filenames:

                print "Checking %s..." % f

                reader = csv.DictReader(open(f), delimiter='\t')

                data_set = []
                for row in reader:
                    data = {}

                    if 'Title' in row:
                        appname = row['Title'].strip()
                    elif 'Title / Episode / Season' in row:
                        appname = row['Title / Episode / Season'].strip()
                    else:
                        raise ValueError

                    data['appname'] = appname

                    if 'SKU' in row:
                        sku = row['SKU'].strip()
                    elif 'Vendor Identifier' in row:
                        sku = row['Vendor Identifier'].strip()
                    else:
                        raise ValueError
                    data['sku'] = sku

                    if 'Apple Identifier' in row:
                        appleid = row['Apple Identifier']
                    else:
                        raise ValueError

                    data['appleid'] = appleid
                    data_set.append(data)

                for data in data_set:

                    app_id, created = App.objects.get_or_create(sku=data['sku'])
                    if created:
                        app_id.name = data['appname']
                        app_id.appleid = data['appleid']
                        app_id.save()
                    else:
                        if app_id.appleid is None:
                            app_id.appleid = data['appleid']
                            app_id.save()

                if self.check_done():
                    break

        if self.check_done():
            print "All done..."
        else:
            print "Not done..."

        pass

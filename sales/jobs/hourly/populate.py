#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/03]

from django_extensions.management.jobs import BaseJob, HourlyJob
from settings import *

class Job(HourlyJob):
    help = "Populate data files in [%s]" % DATA_DIR

    def execute(self):
        import os
        import sys
        import csv
        import re
        import datetime

        from sales.models import App, Date, Sales, Country
        from django.core.mail import mail_admins

        print self.help

        if (DATA_DIR != '' and not os.path.exists(DATA_DIR)):
            os.makedirs(DATA_DIR)

        filenames = [os.path.join(DATA_DIR, f)
                     for f in os.listdir(DATA_DIR)
                     if f.startswith(DAILY_SALES_PREFIX)]

        for f in filenames:
            match = re.findall('S_D_(.*)\.txt', f)
            try:
                date = datetime.datetime.strptime(match[0], '%m-%d-%Y').date()
            except ValueError:
                # for old format data
                try:
                    date = datetime.datetime.strptime(match[0], '%m%d%Y').date()
                except ValueError:
                    continue

            d_id, created = Date.objects.get_or_create(date=date)
            if created:
                d_id.populated = False
            else:
                if d_id.populated == True:
                    continue

            print "[%s] is now processing..." % d_id

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
                data['date'] = datetime.datetime.strptime(row['Begin Date'].strip(), '%m/%d/%Y').date()
                data['units'] = int(row['Units'])

                if 'Developer Proceeds' in row:
                    proceeds = float(row['Developer Proceeds'])
                elif 'Royalty Price' in row:
                    proceeds = float(row['Royalty Price'])
                else:
                    raise ValueError


                data['proceeds'] = float(proceeds)

                country_code = row['Country Code'].strip()
                try:
                    country = Country.objects.get(code=country_code)
                except:
                    country = Country.objects.get(code='ZZ') # unknown

                data['country'] = country

                if 'Currency of Proceeds' in row:
                    currency = row['Currency of Proceeds'].strip()
                elif 'Royalty Currency' in row:
                    currency = row['Royalty Currency'].strip()
                else:
                    raise ValueError

                data['currency'] = currency
                data['price'] = float(row['Customer Price'].strip())
                data['ptype'] = row['Product Type Identifier'].strip()

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

                sales = Sales()
                sales.app = app_id
                sales.date = data['date']
                sales.units = data['units']

                sales.proceeds = data['proceeds']
                sales.country = data['country']
                sales.currency = data['currency']

                sales.price = data['price']
                sales.ptype = data['ptype']
                sales.category = sales.calc_category(data['ptype'], data['price'])

                sales.save()

            d_id.populated = True
            d_id.save()

        pass

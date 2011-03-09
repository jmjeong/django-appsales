#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/03]

from django_extensions.management.jobs import BaseJob, HourlyJob
from settings import *

class Job(BaseJob):
    help = "Download sales data from iTunesStore"

    def execute(self):
        import utils.appdailysales 

        # download daily report
        options = utils.appdailysales.ReportOptions()
        options.unzipFile = True
        options.verbose = False

        for i in ACCOUNT_INFO:
            options.appleId = i['APPSTORE_ID']
            options.password = i['APPSTORE_PW']
            options.outputDirectory = i['DATA_DIR']

            filenames = utils.appdailysales.downloadFile(options)
            
            print 'Report file downloaded: \n%s' % filenames

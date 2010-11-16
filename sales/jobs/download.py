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
    
        options.appleId = APPSTORE_ID
        options.password = APPSTORE_PW
        options.outputDirectory = DATA_DIR
        options.unzipFile = True
        options.verbose = False

        filenames = utils.appdailysales.downloadFile(options)
        print 'Report file downloaded: \n%s' % filenames

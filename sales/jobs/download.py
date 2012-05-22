#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/03]

from settings import *
from django_extensions.management.jobs import BaseJob, HourlyJob
import os.path
import subprocess
import sys
import datetime
import gzip
import os

class Job(BaseJob):
    help = "Download sales data from iTunesStore"

    def setupDir(self, downloadDir):
        if (downloadDir != '' and not os.path.exists(downloadDir)):
            os.makedirs(downloadDir)

    def downloadUsingAutoIngest(self, appId, appPw, vendorId, downloadDir):
        # check the file
        
        if not os.path.exists(AUTO_INGESTION_PROGRAM):
            print "%s is not Exists" % AUTO_INGESTION_PROGRAM
            sys.exit(1)

        self.setupDir(downloadDir)

        autoIngestionDir =  os.path.dirname(AUTO_INGESTION_PROGRAM)
        autoIngestionProg = os.path.splitext(os.path.basename(AUTO_INGESTION_PROGRAM))[0]

        today = datetime.datetime.now()
        start_date = today + datetime.timedelta(days=-7)
        end_date = today + datetime.timedelta(days=1)

        downloadFiles = []

        for day in range(-14, 0):
            date = today+datetime.timedelta(days=day)

            filename = os.path.join(downloadDir, DAILY_SALES_PREFIX+date.strftime("%m-%d-%Y")+'.txt')
            if os.path.exists(filename):
                continue

            downloadFiles.append([date, filename])

        for job in downloadFiles:
            program = 'java -cp %s %s %s %s %d Sales Daily Summary %s' \
                      % (autoIngestionDir, autoIngestionProg, appId, appPw, vendorId,
                         job[0].strftime("%Y%m%d") )

            output = subprocess.check_output(program.split()) 

            if "File Downloaded Successfully" in output:
                print "Success : %s data" % job[0].strftime("%Y-%m-%d")
            else:
                print "Nope    : %s data" % job[0].strftime("%Y-%m-%d")
                continue

            downloadFileName = output.split()[0]
            f = gzip.open(downloadFileName, 'rb')
            content = f.read()
            f.close()

            out = open(job[1], 'wb')
            out.write(content)
            out.close()

            os.remove(downloadFileName)

        pass

    def execute(self):

        for i in ACCOUNT_INFO:
            self.downloadUsingAutoIngest(i['APPSTORE_ID'],
                                         i['APPSTORE_PW'],
                                         i['VENDOR_ID'],
                                         i['DATA_DIR'])

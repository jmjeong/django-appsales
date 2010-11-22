#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/03]

from django_extensions.management.jobs import BaseJob
from settings import *
import urllib
import urllib2
import re

from sales.models import App, Date, Sales, Country

class Job(BaseJob):
    help = "Download Reviews about application"

    def readHtml(self, opener, url):
        request = urllib2.Request(url, None)
        urlHandle = opener.open(request)
        html = urlHandle.read()
        return html

    def execute(self):
        # download daily report
        

        opener = urllib2.build_opener()
 
        opener.addheaders = [('user-agent', 'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)'),]
        opener.addheaders = [('X-Apple-Store-Front', '143466-1'),]


        # urlBase = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&pageNumber=0&sortOrdering=4&type=Purple+Software"
        urlBase = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&sortOrdering=4&type=Purple+Software"

        for app in App.objects.values('appleid'):

            urlWebsite = urlBase % app['appleid']
            
            request = urllib2.Request(urlWebsite)
            urlHandle = opener.open(request)

            content = self.readHtml(opener, urlWebsite)

            while True:
                try:
                    g  = re.search(r'<TextView topInset="0" truncation="right" leftInset="0" squishiness="1" styleSet="basic13" textJust="left" maxLines="1">.*<b>(.*)</b>.*</TextView>', content)
                    print g.group(1)

                    content = content[g.end():]
                    g = re.search(r'<HBoxView topInset="1" alt="(.*)">', content)
                    print g.group(1)

                    content = content[g.end():]
                    g = re.search(r'viewUsersUserReviews.*?>.*?<b>\s*?(.*?)\s*?</b>.*?</GotoURL>\s*-\s*Version\s(.*?)-(.*?)</SetFontStyle>', content, re.M|re.S)
                    print g.group(1).strip(), g.group(2).strip(), g.group(3).strip()

                    content = content[g.end():]
                    g = re.search(r'<SetFontStyle normalStyle="textColor">(.*?)</SetFontStyle>', content, re.M|re.S)
                    print g.group(1).strip()
                    content = content[g.end():]

                    print "--"*10
                except:
                    break
            break


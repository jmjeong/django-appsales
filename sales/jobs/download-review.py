#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/23]

from django_extensions.management.jobs import BaseJob
from settings import *
import urllib
import urllib2
import re
import datetime

from sales.models import App, Date, Sales, Country, Review

class Job(BaseJob):
    help = "Download Reviews about application"

    COUNTRY_CODE = (
        ( "kr", "143466", "%d-%b-%Y"),
        # ( "us", "143441", '%b %d, %Y'),
        # ( "hk", "143463", "%d-%b-%Y"),
        # ( "jp", "143462", "%d-%b-%Y"),
        # ( "au", "143460", "%d-%b-%Y"),
        # ( "de", "143443", "%d.%m.%Y"),
        # ( "gb", "143444", "%d-%b-%Y"),
        # ( "fr", "143442", "%d %b %Y"),
        # ( "ch", "143459", "%d-%b-%Y")
        )

    def read_html(self, opener, url):
        request = urllib2.Request(url, None)
        urlHandle = opener.open(request)
        html = urlHandle.read()
        return html

    def extract_review(self, content):
        reviews = []

        while True:
            review = {}
            g  = re.search(r'<TextView topInset="0" truncation="right" leftInset="0" squishiness="1" styleSet="basic13" textJust="left" maxLines="1">.*<b>(.*)</b>.*</TextView>', content)
            if g:
                review['title'] = g.group(1).strip()
                content = content[g.end():]
            else:
                break
            

            g = re.search(r'<HBoxView topInset="1" alt="(.*)">', content)
            if g:
                review['stars'] = int(re.search("(\d)", g.group(1)).group(1))
                content = content[g.end():]
            else:
                break
            
            g = re.search(r'viewUsersUserReviews.*?>.*?<b>\s*?(.*?)\s*?</b>.*?</GotoURL>\s*-\s*Version\s(.*?)-(.*?)</SetFontStyle>', content, re.M|re.S)
            if g:
                review['name'] = g.group(1).strip()
                review['version'] = g.group(2).strip()
                review['date'] = g.group(3).strip()
                content = content[g.end():]
            else:
                break
            
            g = re.search(r'<SetFontStyle normalStyle="textColor">(.*?)</SetFontStyle>', content, re.M|re.S)
            if g:
                review['content'] = g.group(1).strip()
                content = content[g.end():]
            else:
                break

            reviews.append(review)

        return reviews
            
    def execute(self):
        # download reviews per application

        opener = urllib2.build_opener()
 
        opener.addheaders = [('user-agent', 'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)'),]
        opener.addheaders = [('X-Apple-Store-Front', '143466-1'),]

        urlBase = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&&pageNumber=%d&sortOrdering=4&type=Purple+Software"

        for cc in self.COUNTRY_CODE:
            print cc
            
            for app in App.objects.all():

                # change store name
                opener.addheaders = [('X-Apple-Store-Front', '%s-1' % cc[1] ),]
                try:
                    country = Country.objects.get(code = cc[0].upper())
                except DoesNotExist:
                    print cc[0], " does not exist"
                    continue

                # app = App.objects.get(name='iHappyDays')

                count = 0
                reviews_all = []

                while True:

                    urlWebsite = urlBase % (app.appleid, count)

                    request = urllib2.Request(urlWebsite)
                    urlHandle = opener.open(request)
                    content = self.read_html(opener, urlWebsite)

                    reviews = self.extract_review(content)
                    if len(reviews) > 0:
                        reviews_all.extend(reviews)
                        count += 1
                    else:
                        break

                print app.name, len(reviews_all)

                for r in reviews_all:
                    date = datetime.datetime.strptime(r['date'], cc[2])                    
                    try:
                        Review.objects.get(app=app, country=country, title=r['title'], stars=r['stars'],
                                           reviewer = r['name'], version = r['version'], date = date)
                        print "pass ... [%s]" % r['title']
                        continue
                    except Review.DoesNotExist:
                        pass
                    
                    entry = Review()
                    entry.app = app
                    entry.country = country
                    entry.title = r['title']
                    entry.stars = r['stars']
                    entry.reviewer = r['name']
                    entry.version = r['version']
                    entry.date = date
                    entry.content = r['content']

                    entry.save()


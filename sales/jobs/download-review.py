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
import sys
from threading import Thread

from sales.models import App, Date, Sales, Country, Review

rtitle = re.compile(r'<TextView topInset="0" truncation="right" leftInset="0" squishiness="1" styleSet="basic13" textJust="left" maxLines="1">.*<b>(.*)</b>.*</TextView>')
rstar = re.compile(r'<HBoxView topInset="1" alt="(.*)">')
rname = re.compile(r'viewUsersUserReviews.*?>.*?<b>\s*?(.*?)\s*?</b>.*?</GotoURL>\s*-\s*Version\s(.*?)-(.*?)</SetFontStyle>', re.M|re.S)
rcontent = re.compile(r'<SetFontStyle normalStyle="textColor">(.*?)</SetFontStyle>', re.M|re.S)

COUNTRY_CODE = (
    ( "kr", "143466", "%d-%b-%Y"),
    ( "us", "143441", '%b %d, %Y'),
    ( "hk", "143463", "%d-%b-%Y"),
    ( "jp", "143462", "%d-%b-%Y"),
    ( "au", "143460", "%d-%b-%Y"),
    ( "de", "143443", "%d.%m.%Y"),
    ( "gb", "143444", "%d-%b-%Y"),
    # ( "fr", "143442", "%d %b %Y"),
    ( "ch", "143459", "%d-%b-%Y")
    )

class download_report(Thread):
    def __init__(self, app, country):
        Thread.__init__(self)
        self.country = country
        self.app = app;
        self.status = -1
        self.reviews = []

    def read_html(self, opener, url):
        request = urllib2.Request(url, None)
        urlHandle = opener.open(request)
        html = urlHandle.read()
        return html

    def extract_review(self, content):
        global rtitle, rstar, rname, rcontent
        
        reviews = []

        while True:
            review = {}
            g  = rtitle.search(content)
            if g:
                review['title'] = g.group(1).strip()
                content = content[g.end():]
            else:
                break
            
            g = rstar.search(content)
            if g:
                review['stars'] = int(re.search("(\d)", g.group(1)).group(1))
                content = content[g.end():]
            else:
                print g
                sys.exit(0)
                break
            
            g = rname.search(content)
            if g:
                review['name'] = g.group(1).strip()
                review['version'] = g.group(2).strip()
                review['date'] = g.group(3).strip()
                content = content[g.end():]
            else:
                break
            
            g = rcontent.search(content)
            if g:
                review['content'] = g.group(1).strip()
                content = content[g.end():]
            else:
                break

            reviews.append(review)

        return reviews
        

    def run(self):
        urlBase = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&&pageNumber=%d&sortOrdering=4&type=Purple+Software"

        # print "Downloading Reviews from [%s] about %s..." % (self.country[0].upper(), self.app.name)
        
        opener = urllib2.build_opener()
        opener.addheaders = [('user-agent', 'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)'),]
        opener.addheaders = [('X-Apple-Store-Front', '%s-1' % self.country[1]),]
        try:
            country = Country.objects.get(code = self.country[0].upper())
        except DoesNotExist:
            print cc[0], " does not exist"
            return

        count = 0
        
        while True:
            urlWebsite = urlBase % (self.app.appleid, count)

            request = urllib2.Request(urlWebsite)
            urlHandle = opener.open(request)
            content = self.read_html(opener, urlWebsite)

            reviews = self.extract_review(content)
            if len(reviews) > 0:
                self.reviews.extend(reviews)
                count += 1

                # check for saving time (it is sufficient to check the first item)
                try:
                    r = reviews[0]
                    try:
                        date = datetime.datetime.strptime(r['date'], self.country[2])
                    except:
                        print "*" * 50
                        print "Error: %s, %s" % (r['date'], self.country[2])
                        date = None
                        pass
                    Review.objects.get(app=self.app, country=country, title=r['title'], stars=r['stars'],
                                       reviewer = r['name'], version = r['version'], date = date)
                    break
                except Review.DoesNotExist: 
                    pass
            else:
                break
        
class Job(BaseJob):
    help = "Download Reviews about application"
            
    def execute(self):
        # download reviews per application
        global COUNTRY_CODE

        download_thread = []
        
        for cc in COUNTRY_CODE:
            for app in App.objects.all():
                thread = download_report(app, cc)
                download_thread.append(thread)
                thread.start()

        for thread in download_thread:
            thread.join()

            # print "%s from [%s] : %d" % (thread.app.name, thread.country[0].upper(),len(thread.reviews))

            for r in thread.reviews:
                date = datetime.datetime.strptime(r['date'], thread.country[2])                    
                try:
                    Review.objects.get(app=thread.app, title=r['title'], stars=r['stars'],
                                       reviewer = r['name'], version = r['version'], date = date)
                    # print "pass ... [%s]" % r['title']
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

                print "add  ... [%s]" % r['title']

                entry.save()


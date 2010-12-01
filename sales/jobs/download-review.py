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
    def __init__(self, app, country, appleid, countryname, countrycode, dateformat):
        Thread.__init__(self)

        # Foreign key
        self.app = app
        self.country = country
        
        self.appleid = appleid
        self.countrycode = countrycode
        self.countryname = countryname
        self.dateformat = dateformat
        
        # output
        self.reviews = []

    def __read_html(self, opener, url):
        request = urllib2.Request(url, None)
        urlHandle = opener.open(request)
        html = urlHandle.read()
        return html

    def __extract_review(self, content):
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

    def __check_exists(self, r):
        try:
            Review.objects.get(app=self.app, country=self.country, title=r['title'], stars=r['stars'],
                               reviewer = r['name'], version = r['version'])
            return True
        except Review.DoesNotExist: 
            return False

    def __post_process(self, reviews, app, country, dateformat):
        for r in reviews:
            r['app'] = app
            r['country'] = country
            try:
                r['date'] = datetime.datetime.strptime(r['date'], dateformat)
            except AttributeError:
                print r['date'], dateformat
                pass

    def run(self):
        urlBase = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&&pageNumber=%d&sortOrdering=4&type=Purple+Software"

        opener = urllib2.build_opener()
        opener.addheaders = [('user-agent', 'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)'),]
        opener.addheaders = [('X-Apple-Store-Front', '%s-1' % self.countrycode),]

        count = 0
        
        while True:
            urlWebsite = urlBase % (self.appleid, count)

            request = urllib2.Request(urlWebsite)
            urlHandle = opener.open(request)
            content = self.__read_html(opener, urlWebsite)

            reviews = self.__extract_review(content)

            # convert date format, add foreign key for app, country
            self.__post_process(reviews, self.app, self.country, self.dateformat)
            self.reviews.extend(reviews)

            # if exists, download the next page 
            if len(reviews) > 0 and not self.__check_exists(reviews[0]):
                count += 1
            else:
                break
        
class Job(BaseJob):
    help = "Download Reviews about application"
            
    def execute(self):
        # download reviews per application

        download_thread = []
        
        for cc in COUNTRY_CODE:
            try:
                country = Country.objects.get(code = cc[0].upper())
            except Country.DoesNotExist:
                print cc[0], " does not exist"
                raise Exception

            for app in App.objects.all():
                thread = download_report(app, country, app.appleid,
                                         countryname=cc[0], countrycode=cc[1], dateformat=cc[2])
                download_thread.append(thread)
                thread.start()

        for thread in download_thread:
            thread.join()

            print "%s from [%s] : %d" % (thread.app.name.encode('utf-8'), thread.countryname, len(thread.reviews))
            for r in thread.reviews:
                try:
                    Review.objects.get(app=r['app'], country=r['country'], title=r['title'],
                                       stars=r['stars'], reviewer = r['name'],
                                       version = r['version'], date = r['date'])
                    # print "pass ... [%s]" % r['title']
                    continue
                except Review.DoesNotExist:
                    pass

                entry = Review()
                entry.app = r['app']
                entry.country = r['country']
                entry.title = r['title']
                entry.stars = r['stars']
                entry.reviewer = r['name']
                entry.version = r['version']
                entry.date = r['date']
                entry.content = r['content']

                print "add  ... [%s]" % r['title']

                entry.save()


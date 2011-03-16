#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Jaemok Jeong(jmjeong@gmail.com)
#
# [2011/03/14]

import urllib,urllib2
import sys
import datetime

try:
    import json
except ImportError:
    raise ImportError, "Python 2.6+ has built-in json module"

class AdmobNetworkErrorException(Exception):
    pass

class AdmobErrorException(Exception):
    pass

class AdmobApi(object):
    """
    Retrieve Admob information
    """

    def __init__(self, client_key=''):
        self.client_key = client_key
        self.opener = urllib2.build_opener()

    def login(self, email, pw):
        urlBase = 'https://api.admob.com/v2/auth/login'
    
        requestData = urllib.urlencode({
            'client_key': self.client_key,
            'email': email,
            'password' : pw,
        })

        try:
            urlHandle = self.opener.open(urlBase, requestData)
        except urllib2.HTTPError, urlib2.URLError:
            raise AdmobNetworkErrorException

        result = json.loads(urlHandle.read())

        if not result['errors']:
            return result['data']['token']
        else:
            print result['errors']
            raise AdmobErrorException


    def search(self, token):
        urlBase = 'https://api.admob.com/v2/site/search?%s'
        requestData = urllib.urlencode({
            'client_key': self.client_key,
            'token': token,
        })
        requestUrl = urlBase % requestData

        try:
            urlHandle = self.opener.open(requestUrl)
        except urllib2.HTTPError, urlib2.URLError:
            raise AdmobNetworkErrorException

        result = json.loads(urlHandle.read())

        if not result['errors']:
            return result['data']
        else:
            print result['errors']
            raise AdmobErrorException

    def stats(self, token, id, start_date, end_date):
        urlBase = 'https://api.admob.com/v2/site/stats?%s'
        requestData = urllib.urlencode({
            'client_key': self.client_key,
            'token': token,
            'site_id': id,
            'start_date': start_date,
            'end_date': end_date,
            'time_dimension' : 'day',
            
        })
        requestUrl = urlBase % requestData

        try:
            urlHandle = self.opener.open(requestUrl)
        except urllib2.HTTPError, urlib2.URLError:
            raise AdmobNetworkErrorException

        result = json.loads(urlHandle.read())

        if not result['errors']:
            return result['data']
        else:
            print result['errors']
            raise AdmobErrorException

if __name__ == '__main__':
    client_key = ''                     # client key
    email = ''                          # email id
    passwd = ''                         # pw

    admob = AdmobApi(client_key)
    token = admob.login(email, passwd)

    today = datetime.datetime.now()
    # start_date = datetime.date(2009,1,1)
    start_date = today + datetime.timedelta(days=-7)
    end_date = today + datetime.timedelta(days=1)

    result = admob.search(token)
    for i in result:
        print admob.stats(token, id=i['id'],
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d'))

    pass

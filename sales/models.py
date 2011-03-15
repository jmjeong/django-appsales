#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jaemok Jeong(jmjeong@gmail.com)
#
# [2010/11/05]

from django.db import models
import datetime

# Create your models here.

class App(models.Model):
    appleid = models.CharField(max_length=18)
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Date(models.Model):
    account = models.CharField(max_length=256)
    date = models.DateField()
    populated = models.BooleanField()
    
    created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.date.strftime('%Y/%m/%d')

class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.code

class Review(models.Model):
    app = models.ForeignKey(App)

    country = models.ForeignKey(Country)
    
    title = models.CharField(max_length=256)
    stars = models.IntegerField()
    reviewer = models.CharField(max_length=256)
    version = models.CharField(max_length=100)
    date = models.DateField()       
    content = models.TextField()
    
    created = models.DateTimeField(auto_now=True)

class Sales(models.Model):
    TYPE_CHOICES = (
        ('1', 'Free or Paid Apps'),
        ('7', 'Updates'),
        ('IA1', 'In Apps Purchase'),
        ('IA9', 'In Apps Subscription'),
        ('1F', '(Universal)Free or Paid Apps'),
        ('7F', '(Universal)Updates'),
        ('1T', '(iPad)Free or Paid Apps'),
        ('7T', '(iPad)Updates'))

    TYPE_CALC_CHOICES = (
        ('FR', 'Free Apps'),
        ('UP', 'Updates'),
        ('IA', 'In Apps Purchase'),
        ('PA', 'Paid Apps'),
        ('ER', 'None'),
        )

    TYPE_CURRENCY = (
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('DKK', 'Danish Kroner'),
        ('EUR', 'European Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('MXN', 'Maxican Peso'),
        ('NOK', 'Norwegian Kroner'),
        ('NZD', 'New Zealand Dollar'),
        ('SEK', 'Swedish Kronor'),
        ('USD', 'United States Dollar'))
    
    app = models.ForeignKey(App)
    date = models.DateField()
    units = models.IntegerField()
    proceeds = models.FloatField()
    country = models.ForeignKey(Country)
    currency = models.CharField(max_length=3)
    price = models.FloatField()
    ptype = models.CharField(max_length=3, choices=TYPE_CHOICES)
    category = models.CharField(max_length=2, choices=TYPE_CALC_CHOICES)
    
    def calc_category(self, ptype, price):
        if ptype == '1' or ptype == '1F' or ptype == '1T':
            if price == 0:
                return "FR"
            else:
                return "PA"
        elif ptype == 'IA1' or ptype == 'IA9':
            return 'IA'
        elif '7' in ptype:
            return 'UP'
        else:
            return "ER"
        

    def __unicode__(self):
        return self.app.name + "(" + self.date.strftime('%m/%d') + ")"
    
class Admob(models.Model):
    app = models.ForeignKey(App)
    date = models.DateField()

    requests = models.IntegerField()
    overall_requests = models.IntegerField()
    housead_requests = models.IntegerField()
    interstitial_requests = models.IntegerField()
    impressions = models.IntegerField()
    cpc_impressions = models.IntegerField()
    cpm_impressions = models.IntegerField()
    exchange_impressions = models.IntegerField()
    housead_impressions = models.IntegerField()
    interstitial_impressions = models.IntegerField()
    fill_rate = models.FloatField()
    housead_fill_rate = models.FloatField()
    overall_fill_rate = models.FloatField()
    clicks = models.IntegerField()
    housead_clicks = models.IntegerField()
    ctr = models.FloatField()
    housead_ctr = models.FloatField()
    ecpm = models.FloatField()
    revenue = models.FloatField()
    cpc_revenue = models.FloatField()
    cpm_revenue = models.FloatField()
    exchange_downloads = models.IntegerField()

    # def __unicode__(self):
    #     return self.date.strftime('%Y/%m/%d')

    def __unicode__(self):
        return self.app.name + " (" + self.date.strftime('%m/%d') + ")"
    

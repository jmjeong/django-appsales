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
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Date(models.Model):
    date = models.DateTimeField(unique=True)
    populated = models.BooleanField()
    created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.date.strftime('%Y/%m/%d')

class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.code

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
    date = models.DateTimeField()
    units = models.IntegerField()
    proceeds = models.FloatField()
    country = models.ForeignKey(Country)
    currency = models.CharField(max_length=3)
    price = models.FloatField()
    ptype = models.CharField(max_length=3, choices=TYPE_CHOICES)
    category = models.CharField(max_length=2, choices=TYPE_CALC_CHOICES)
    
    def print_date(self):
        return self.date.date()
    
    print_date.short_description = "Date"

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
    

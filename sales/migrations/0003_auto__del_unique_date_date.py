# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Date', fields ['date']
        db.delete_unique('sales_date', ['date'])


    def backwards(self, orm):
        
        # Adding unique constraint on 'Date', fields ['date']
        db.create_unique('sales_date', ['date'])


    models = {
        'sales.app': {
            'Meta': {'object_name': 'App'},
            'appleid': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sales.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sales.date': {
            'Meta': {'object_name': 'Date'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'populated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'sales.review': {
            'Meta': {'object_name': 'Review'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.App']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reviewer': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'stars': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sales.sales': {
            'Meta': {'object_name': 'Sales'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.App']"}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Country']"}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'proceeds': ('django.db.models.fields.FloatField', [], {}),
            'ptype': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'units': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['sales']

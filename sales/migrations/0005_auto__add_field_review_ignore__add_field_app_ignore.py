# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Review.ignore'
        db.add_column('sales_review', 'ignore', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'App.ignore'
        db.add_column('sales_app', 'ignore', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Review.ignore'
        db.delete_column('sales_review', 'ignore')

        # Deleting field 'App.ignore'
        db.delete_column('sales_app', 'ignore')


    models = {
        'sales.admob': {
            'Meta': {'object_name': 'Admob'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.App']"}),
            'clicks': ('django.db.models.fields.IntegerField', [], {}),
            'cpc_impressions': ('django.db.models.fields.IntegerField', [], {}),
            'cpc_revenue': ('django.db.models.fields.FloatField', [], {}),
            'cpm_impressions': ('django.db.models.fields.IntegerField', [], {}),
            'cpm_revenue': ('django.db.models.fields.FloatField', [], {}),
            'ctr': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'ecpm': ('django.db.models.fields.FloatField', [], {}),
            'exchange_downloads': ('django.db.models.fields.IntegerField', [], {}),
            'exchange_impressions': ('django.db.models.fields.IntegerField', [], {}),
            'fill_rate': ('django.db.models.fields.FloatField', [], {}),
            'housead_clicks': ('django.db.models.fields.IntegerField', [], {}),
            'housead_ctr': ('django.db.models.fields.FloatField', [], {}),
            'housead_fill_rate': ('django.db.models.fields.FloatField', [], {}),
            'housead_impressions': ('django.db.models.fields.IntegerField', [], {}),
            'housead_requests': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impressions': ('django.db.models.fields.IntegerField', [], {}),
            'interstitial_impressions': ('django.db.models.fields.IntegerField', [], {}),
            'interstitial_requests': ('django.db.models.fields.IntegerField', [], {}),
            'overall_fill_rate': ('django.db.models.fields.FloatField', [], {}),
            'overall_requests': ('django.db.models.fields.IntegerField', [], {}),
            'requests': ('django.db.models.fields.IntegerField', [], {}),
            'revenue': ('django.db.models.fields.FloatField', [], {})
        },
        'sales.app': {
            'Meta': {'object_name': 'App'},
            'appleid': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'ignore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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

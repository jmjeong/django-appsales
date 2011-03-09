# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'App'
        db.create_table('sales_app', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appleid', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('sales', ['App'])

        # Adding model 'Date'
        db.create_table('sales_date', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(unique=True)),
            ('populated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('sales', ['Date'])

        # Adding model 'Country'
        db.create_table('sales_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('sales', ['Country'])

        # Adding model 'Review'
        db.create_table('sales_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.App'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Country'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('stars', self.gf('django.db.models.fields.IntegerField')()),
            ('reviewer', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('sales', ['Review'])

        # Adding model 'Sales'
        db.create_table('sales_sales', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.App'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('units', self.gf('django.db.models.fields.IntegerField')()),
            ('proceeds', self.gf('django.db.models.fields.FloatField')()),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Country'])),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('ptype', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('sales', ['Sales'])


    def backwards(self, orm):
        
        # Deleting model 'App'
        db.delete_table('sales_app')

        # Deleting model 'Date'
        db.delete_table('sales_date')

        # Deleting model 'Country'
        db.delete_table('sales_country')

        # Deleting model 'Review'
        db.delete_table('sales_review')

        # Deleting model 'Sales'
        db.delete_table('sales_sales')


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
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
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

import os
import sys

# add your path
sys.path.append('/var/www/appsales')
sys.path.append('/var/www')

os.environ['DJANGO_SETTINGS_MODULE'] = 'appsales.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
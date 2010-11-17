import os.path
from django.conf.urls.defaults import *
from sales.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media')

urlpatterns = patterns(
    '',
    # Example:
    # (r'^appsales/', include('appsales.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # main page
    (r'^(s/(?P<sort>\w+)/)?$', main_page),
    (r'^app/(?P<appid>\d+)(/s/(?P<sort>\w+))?(/(?P<json>chart\.json))?/$', app_page),

    # session
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),

    # site media
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     { 'document_root' : site_media}),
)

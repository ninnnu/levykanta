from django.conf.urls.defaults import patterns, include, url

from django.db.models.loading import cache as model_cache
if not model_cache.loaded:
    model_cache.get_models()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Levykanta.views.home', name='home'),
    url(r'^discdb/$', 'discdb.views.index'),
    url(r'^discdb/from/(?P<author_id>\d+)/$', 'discdb.views.show_by_author'),
    url(r'^discdb/add/$', 'discdb.views.add_disc'),
    url(r'^discdb/suggest/$', 'discdb.views.suggest'),
    url(r'^discdb/suggest/catalogue/$', 'discdb.views.suggest_cataloged'),
    url(r'^discdb/show/(?P<cd_id>\d+)/$', 'discdb.views.show'),
    url(r'^discdb/track/add/$', 'discdb.views.add_track'),
    # url(r'^discdb/lookup/(?P<barcode>\d+)/$', 'discdb.views.lookup_code'),
    url(r'^discdb/lookup/catalogue/(?P<cd_id>\d+)/$', 'discdb.views.lookup_catalogue'),
    url(r'^discdb/lookup/cd/(?P<cd_id>\d+)/$', 'discdb.views.lookup_cdid'),
    url(r'^discdb/search/$', 'discdb.views.search_view'),
    url(r'^discdb/login/$', 'discdb.views.login_view'),
    url(r'^discdb/request/$', 'discdb.views.wish'),
    url(r'^discdb/show_requests/$', 'discdb.views.show_wishes'),
    url(r'^discdb/done/$', 'discdb.views.grant_wish'),
    url(r'^discdb/return/$', 'discdb.views.return_disc'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

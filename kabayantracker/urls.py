from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kabayantracker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('',	
    (r'(?:.*?/)?(?P<path>(admin|css|img|js)/.+)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),
	(r'(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
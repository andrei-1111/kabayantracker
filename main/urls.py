
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^grab$', 'grab_view', name='grab'),
    
    url(r'^process_message$', 'process_message', name='process_message'),
    url(r'^process_response$', 'process_response', name='process_response'),

)
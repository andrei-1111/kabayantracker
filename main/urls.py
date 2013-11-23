
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^grab$', 'grab', name='grab'),

)
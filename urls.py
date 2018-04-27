# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import index

urlpatterns = [
    url(r'(?P<_evento>[-\w]+)/(?P<_content>[-\w]+)/$', index, name='index'),
    url(r'(?P<_evento>[-\w]+)/$', index, name='index'),
    ]
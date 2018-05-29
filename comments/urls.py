# -*- coding: utf-8 -*-
from django.conf.urls import include,url
from . import views
app_name='comments'
urlpatterns=[
    url(r'^comment/post/(?P<pk>[0-9]+)/$',views.comments,name='comments'),


]
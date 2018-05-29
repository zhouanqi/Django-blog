# -*- coding: utf-8 -*-
from django.conf.urls import include,url
from . import views
app_name='blog'
urlpatterns=[
    url(r'^$',views.Indexview.as_view(),name='index'),
    url(r"^post/(?P<pk>[0-9]+)/$",views.Postdetailview.as_view(),name='detail'),
    # url(r"^post/(?P<pk>[0-9]+)/$",views.detail,name='detail'),
    url(r"^getPostdate/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$",views.Postdateview.as_view(),name='getPostdate'),
    url(r"^getCategory/(?P<pk>[0-9]+)/$",views.Categoryviews.as_view(),name='getCategory'),
    url(r"^getTag/(?P<pk>[0-9]+)/$",views.Tagviews.as_view(),name='getTag'),
    # url(r"^search/$",views.Seachviews.as_view,name="search"),
    #url(r'^search/$', views.search, name='search'),
]
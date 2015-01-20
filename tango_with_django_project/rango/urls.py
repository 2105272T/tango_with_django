from django.conf.urls import patterns, url
from rango import views

# At the top of your urls.py file, add the following line:
from django.conf import settings

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about',views.about, name='about'))


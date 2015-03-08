from django.conf.urls import patterns, url
from rango import views

# At the top of your urls.py file, add the following line:
from django.conf import settings

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about', views.about, name='about'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/', views.add_page, name='add_page'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^goto/$', views.track_url, name='goto'),
        url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
        url(r'^add_profile/(?P<username>[\w\-]+)/$', views.register_profile, name='add_profile'),
        url(r'^search_users/$', views.search_users, name='search_users'),

        )



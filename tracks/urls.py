from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TrackList().as_view()),
    url(r'^report/weekly/$', views.WeeklyReport().as_view()),
    url(r'^destroy/(?P<pk>[0-9]+)/$', views.TrackDestroy().as_view()),
    url(r'^update/(?P<pk>[0-9]+)/$', views.TrackUpdate().as_view()),
]

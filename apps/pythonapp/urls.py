from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='login'),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^success$', views.success),
	url(r'^logout$', views.logout),
    url(r'^main$', views.main, name='pythonapp'),
    url(r'^planner$', views.planner, name='planner'),
    url(r'^show/(?P<id>\d+)$', views.show, name='show'),
    url(r'^addnew$', views.addnew, name='addnew'),
    url(r'^jointr/(?P<id>\d+)$', views.jointr, name='jointr'),
    url(r'^others$', views.others, name='others')
]

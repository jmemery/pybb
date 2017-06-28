from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.pythonapp.urls')),
    url(r'^travel/', include('apps.travel.urls')),

]
""" unless you're adding a new app dont change this page """

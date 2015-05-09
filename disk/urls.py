from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', views.home, name='home'),
    url(r'^$', views.index, name='index'),
    url(r'^Project(?P<project_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^createProject$', views.createProject, name='createProject'),
    url(r'^Project(?P<project_id>[0-9]+)/Version(?P<version_id>[0-9]+)/$', 
            views.instruction, name='instruction'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, 
                        document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT)
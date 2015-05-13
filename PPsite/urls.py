from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^disk/', include('disk.urls', namespace='disk')),

    url(r'^signin/', views.sign_in, name='sign_in'),
    url(r'^signout/', views.sign_out, name='sign_out'),
    url(r'^signup/', views.sign_up, name='sign_up'),
    url(r'^deleteVersion(?P<version_id>[0-9]+)/$', views.deleteVersion, name='deleteVersion'),
    url(r'^deleteProject(?P<project_id>[0-9]+)/$', views.deleteProject, name='deleteProject'),

    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, 
                        document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT)
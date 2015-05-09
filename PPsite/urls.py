from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^signin/', views.sign_in, name='sign_in'),

    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, 
                        document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT)
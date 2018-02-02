from django.conf.urls import include, url
from django.contrib import admin

from Kryptism import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Kryptism.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dwok/', include('decryptionwithoutkey.urls', namespace="dwok")),
    url(r'^dwk/', include('decryptionwithkey.urls', namespace="dwk")),
    url(r'^en/', include('encryption.urls', namespace="en")),
    url(r'^', views.home,name='home'),
]

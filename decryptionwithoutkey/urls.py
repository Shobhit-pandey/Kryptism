from django.conf.urls import include, url

from decryptionwithoutkey import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Kryptism.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.home, name='home'),
    url(r'^ceasor/$', views.filter_ceasor, name='ceasor'),
    url(r'^vigenere/$', views.vigenere, name='vigenere'),
]

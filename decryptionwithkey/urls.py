from django.conf.urls import include, url

from decryptionwithkey import views

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^ceasor/$', views.ceasor, name='ceasor'),
    url(r'^sdes/$', views.sdes, name='sdes'),
    url(r'^hill-cipher/$', views.hillcipher, name='hillcipher'),
    url(r'^vigenere/$', views.vigenere, name='vigenere'),
    url(r'^playfair/$', views.playfair, name='playfair'),
    url(r'^des/$', views.des, name='des'),
    url(r'^triple-des/$', views.tripledes, name='tripledes'),
    url(r'^substitution/$', views.substitution, name='substitution'),
    url(r'^railfence/$', views.railfence, name='railfence'),
    url(r'^rsa/$', views.rsa, name='rsa'),
]

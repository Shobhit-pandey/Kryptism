from django.conf.urls import include, url

from encryption import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Kryptism.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.enhome, name='enhome'),
    url(r'^ceasor/', views.ceasor, name='ceasor'),
]

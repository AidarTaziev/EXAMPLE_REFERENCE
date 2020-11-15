from django.conf import settings
from django.conf.urls import url
from . import views

app_name = 'authentication'

if settings.LOCAL_SETTINGS:
    urlpatterns = [
        url(r'^login$', views.login, name='login'),
        url(r'^signup$', views.signup, name='signup'),
        url(r'^logout$', views.acc_logout, name='logout'),
        url('', views.login_page, name='main')
    ]




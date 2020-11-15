from django.conf.urls import url
from . import views

app_name = 'django_sso_client'

urlpatterns = [
    url(r'^logout', views.sso_logout),
    url(r'^', views.sso_login)
]

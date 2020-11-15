from django.urls import path
from . import views


urlpatterns = [
    path('(?P<polymerId>\d+)', views.order_polymer),
    path('', views.order_polymer),
]

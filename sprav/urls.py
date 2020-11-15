from django.urls import path
from django.conf.urls import url, include
from . import views
from polymer_order import views as polymer_order_views

urlpatterns = [
    path('order/', include('polymer_order.urls')),
    path('(?P<polymer_id>\d+)', views.show_polymer_properties),
    path('get_analogs_for_polymer_id', views.get_analogs),
    path('get_all_plants_types', views.get_all_plants_types),
    path('get_all_polymers_short_info', views.get_all_polymers_short_info),
    path('get_polymer_short_info', views.get_polymer_short_info),
    path('get_types_ref_polymers', views.get_types_ref_polymers),
    path('find_polymers_for', views.find_polymers_for_plant),
]

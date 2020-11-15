#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from polymer_order.models import *


# Register your models here.

class PolymerOrdersAdmin(admin.ModelAdmin):
    list_display = ['idgoods', 'numbers', 'consignee', 'shipment_from', 'shipment_to', 'idshipment_conditions', 'idshipment_methods',
                  'address', 'contact_name', 'contact_phone', 'contact_email', 'message', 'order_datetime']
    list_display_links = None

    # list_filter =  ('idgoods__subtype__type__name',)
    ordering = ['-order_datetime']

admin.site.register(Orders, PolymerOrdersAdmin)
admin.site.register(ShipmentMethods)
admin.site.register(ShipmentConditions)

admin.site.site_header = "Админка"
admin.site.site_title = ""
# Register your models here.


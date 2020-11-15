#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.mail import send_mail
from polymer_order.models import *
from sprav.models import Polymers
from polymer_order.forms import PolymerOrderForm
from bank_account.requests import get_user_bank_account_info

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename=u'{base_dir}/kartli_reference.log'.format(base_dir=settings.BASE_DIR))


def order_polymer(request, polymer_id=None):
    """
    Контроллер, обеспечивающий форму заказа
    :param request:
    :param polymer_id: id полимера из адрес. строки
    :return: страницу заявки для указанного полимера
    """
    if request.method == 'GET':
        try:
            if polymer_id:
                data = {
                    "polymer_id": polymer_id,
                    "shortcode": Polymers.objects.values('shortcode').get(id=polymer_id)['shortcode'],
                    "shipment_methods": ShipmentMethods.objects.all().order_by('name').values(),
                    "shipment_conditions": ShipmentConditions.objects.all().order_by('id').values(),
                }
                return render(request, "polymer_order/polymer_order.html", context=data)
            else:
                return HttpResponse(status=400)
        except:
            return HttpResponseNotFound('<h1>Полимер не найден</h1>')

    if request.method == 'POST':
        form = PolymerOrderForm(request.POST)

        if form.is_valid():
            saved_form = form.save()
            send_mail(form.cleaned_data)
            return HttpResponse(True)
        else:
            return HttpResponse(False, status=400)

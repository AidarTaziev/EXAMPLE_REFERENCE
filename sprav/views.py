#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from django.http import JsonResponse
from django.conf import settings
from bank_account.requests import get_user_bank_account_info
from sprav.models import *
from sprav.search_polym_methods.search_analogs import get_analogs_for_polymer
from sprav.search_polym_methods.search_polymers import get_search_conditions
from sprav.utils_methods import get_all_selects_data, get_all_polymers_for_type
from sprav.custom_validators import valid_search_filters


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename=u'{base_dir}/kartli_reference.log'.format(base_dir=settings.BASE_DIR))


def search(request):
    """
    Метод-обработчик. Основной метод обрабатывающий поиск
    Если нет выбранных параметров поиска(GET параметров в адресной строке), то тогда
    выводит все полимеры,
    если есть то вызывает другой метод в который передает параметры поиска
    :param request:
    :return: страницу с поиском и результатами поиска
    """
    template_path = 'sprav/main_page.html'
    data = get_all_selects_data()

    if request.method == 'GET':
        if request.GET:
            is_valid, errors_list = valid_search_filters(request.GET)
            if is_valid:
                search_conditions = get_search_conditions(request.GET)
                if search_conditions:
                    data['polymers'] = [polymer.get_full_data() for polymer in Polymers.objects.filter(**search_conditions)]
                else:
                    data['polymers'] = []
            else:
                data['errors_list'] = errors_list
                logging.debug(errors_list)
                return render(request, template_path, context=data)
        else:
            data['polymers'] = [polymer.get_full_data() for polymer in Polymers.objects.all()]

        return render(request, template_path, context=data)
    else:
        return HttpResponse(status=405)


def show_polymer_properties(request, polymer_id=None):
    """
    Выводит свойства данного полимера на отдельной странице
    :param request:
    :param productid:
    :return: страницу 'Свойства полимера'
    """
    if polymer_id:
        try:
            context = Polymers.objects.get(id=polymer_id).get_full_data()
            return render(request, "sprav/polymer/polymer_properties.html", context=context)
        except Exception as ex:
            logging.error(ex)
            return HttpResponseNotFound(status=404)
    else:
        return HttpResponse(status=400)


def get_analogs(request):
    """"
    Выдает аналоги  в  JSON для отдельнго полимера
    Приниммает параметр polymerId
    :return: JSON ответ с аналогами для полимера
    """

    polymer_id = request.GET.get("polymer_id", None)
    if polymer_id:
        analogs = get_analogs_for_polymer(polymer_id)
        data = list(analogs) if analogs else {}

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse(status=400)


@csrf_exempt
def get_all_plants_types(request):
    """
    ВРЕМЕННЫЙ МЕТОД. Возвращает полимеры определенного производителя
    :param plantsName: название компании-производителя
    :return:
    """
    if request.method == 'POST':
        api_secret_key = request.POST['api_secret_key']
        if settings.POLYMER_SPRAV_SECRET_KEY == api_secret_key:
            data = {
                'polymers_plants': list(Plants.objects.values('id', 'name')),
                'polymers_types': list(Types.objects.values('id', 'name'))
            }

            return JsonResponse(data, safe=False)
        else:
            return JsonResponse(status=403)
    else:
        return JsonResponse(status=405)


@csrf_exempt
def get_all_polymers_short_info(request):
    """
    ВРЕМЕННЫЙ МЕТОД. Возвращает полимеры определенного производителя
    :param plantsName: название компании-производителя
    :return:
    """
    if request.method == 'POST':
        api_secret_key = request.POST['api_secret_key']
        if settings.POLYMER_SPRAV_SECRET_KEY == api_secret_key:
            return JsonResponse(list(Polymers.objects.values('id', 'shortcode').order_by('shortcode')), safe=False)
        else:
            return JsonResponse(status=403)
    else:
        return JsonResponse(status=405)


@csrf_exempt
def get_polymer_short_info(request):
    """
    ВРЕМЕННЫЙ МЕТОД. Возвращает полимеры определенного производителя
    :param plantsName: название компании-производителя
    :return:
    """
    if request.method == 'POST':
        api_secret_key = request.POST['api_secret_key']
        if settings.POLYMER_SPRAV_SECRET_KEY == api_secret_key:
            try:
                polymer_id = int(request.POST['polymer_id'])
                if polymer_id:
                    return JsonResponse(
                        Polymers.objects.values('id', 'shortcode', 'subtype__type__id', 'subtype__type__name',
                                                'plants__id', 'plants__name').get(id=polymer_id), safe=False)
                else:
                    return JsonResponse(status=400)
            except Exception as ex:
                logging.warning(ex)

                return JsonResponse(status=500)
        else:
            return JsonResponse(status=403)
    else:
        return JsonResponse(status=405)


@csrf_exempt
def find_polymers_for_plant(request):
    """
    ВРЕМЕННЫЙ МЕТОД. Возвращает полимеры определенного производителя
    :param plantsName: название компании-производителя
    :return:
    """
    if request.method == 'POST':
        api_secret_key = request.POST['api_secret_key']
        if settings.POLYMER_SPRAV_SECRET_KEY == api_secret_key:
            search_conditions = get_search_conditions(request.POST)
            polymers = Polymers.objects.filter(**search_conditions).values('id')
            polymers_ids = [polymer['id'] for polymer in polymers]
            return JsonResponse(polymers_ids, safe=False)
        else:
            return JsonResponse(status=403)
    else:
        return JsonResponse(status=405)


@csrf_exempt
def get_types_ref_polymers(request):
    if request.method == 'POST':
        api_secret_key = request.POST['api_secret_key']
        if settings.POLYMER_SPRAV_SECRET_KEY == api_secret_key:
            types = Types.objects.all().values('id', 'name').order_by('name')
            types_ref_polymers = [{'type': type,
                                   'polymers': list(get_all_polymers_for_type(type['id']))
                                  }
                                  for type in types]

            return JsonResponse(list(types_ref_polymers), safe=False)
        else:
            return JsonResponse(status=403)
    else:
        return JsonResponse(status=405)

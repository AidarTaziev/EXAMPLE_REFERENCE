#!/usr/bin/python
# -*- coding: utf-8 -*-

from decimal import *
from sprav.models import *

DISPLAY_VALUES = ('id', 'shortcode', 'subtype__name', 'plants__name', 'ptr', 'density')


def get_analogs_for_polymer(polymerId):
    """
    Находит аналоги для переданной марки и выводит в виде QuerySet.
    :param polymerId: id марки
    :return: QuerySet с аналогами если они есть или None, если аналоги для данного полимера не были найдены
    """

    if polymerId:
        try:
            currentPolymer = Polymers.objects.get(id=polymerId)
            type = currentPolymer.subtype.type.id
            color = currentPolymer.color
            ptr = currentPolymer.ptr
            density = currentPolymer.density
            copolymer = currentPolymer.copolymer
            subtype = currentPolymer.subtype.id
            subtype_name = currentPolymer.subtype.name
            t_vika = currentPolymer.t_vika
            viscosity_Mooney = currentPolymer.viscosity_Mooney
            diene_content = currentPolymer.diene_content
            ethylene_content = currentPolymer.ethylene_content

            processing_methods = list(
                processing_method.name for processing_method in currentPolymer.processing_methods.all())

            if type == 4:
                analogs = get_analogs_for_polycarbonates(polymerId, type, color, ptr, processing_methods)
            elif type == 1:
                analogs = get_analogs_for_HPP(polymerId, type, color, ptr, density, processing_methods)
            elif type == 2:
                analogs = get_analogs_for_LPP(polymerId, type, subtype, subtype_name, color, ptr, density)
            elif type == 19:
                analogs = get_analogs_for_linnear_poly(polymerId, type, color, copolymer, ptr, density,
                                                       processing_methods)
            elif type == 6:
                analogs = get_analogs_for_polystyrene(polymerId, type, subtype, subtype_name, ptr, t_vika,
                                                      processing_methods)
            elif type == 3:
                analogs = get_analogs_for_polypropylene(polymerId, type, subtype_name, ptr, processing_methods)
            elif type == 7:
                analogs = get_analogs_for_ABS_plastic(polymerId, type, color, ptr, processing_methods)
            elif type == 5:
                analogs = get_analogs_for_PVC(polymerId, type, ptr, density, t_vika, processing_methods)
            elif type == 20:
                analogs = get_analogs_for_rubber(polymerId, type, subtype, viscosity_Mooney, diene_content,
                                                 ethylene_content)

            return analogs
        except Exception as ex:
            print(ex)
            return None

    return None


def get_analogs_for_polycarbonates(polymerId, type, color, ptr, processing_methods):
    """
    Возвращает аналоги для поликарбонатов
    :param polymerId: id марки
    :param type: тип полимера
    :param color: цвет полимера
    :param ptr: ПТР полимера
    :return: QuerySet с аналогами если они есть или None, если аналоги для данного полимера не были найдены
    """

    if processing_methods:
        if 'экструз' in ','.join(map(str, processing_methods)):
            ptrLeft = ptr - ptr / 5
            ptrRigtht = ptr + ptr / 5
        else:
            ptrLeft = ptr - ptr / 10
            ptrRigtht = ptr + ptr / 10
    else:
        ptrLeft = ptr - 2
        ptrRigtht = ptr + 2

    analogs = Polymers.objects.values('id', 'shortcode', 'subtype__name', 'plants__name', 'ptr', 'density'). \
        exclude(id=polymerId).filter(subtype__type=type, color=color, ptr__gte=ptrLeft, ptr__lte=ptrRigtht)

    if len(analogs) == 0:
        return None
    else:
        return analogs


def get_analogs_for_HPP(polymerId, type, color, ptr, density, processing_methods):
    """
    Возвращает аналоги для полиэтиленна высокого давления
    :param polymerId: id марки
    :param type: тип полимера
    :param color: цвет полимера
    :param ptr: ПТР полимера
    :param density: плотность полимера
    :return: QuerySet с аналогами если они есть или None, если аналоги для данного полимера не были найдены
    """

    if processing_methods:
        if 'экструз' in ','.join(map(str, processing_methods)):
            ptrLeft = ptr - ptr / 5
            ptrRigtht = ptr + ptr / 5
        else:
            ptrLeft = ptr - ptr / 10
            ptrRigtht = ptr + ptr / 10
    else:
        ptrLeft = ptr - 2
        ptrRigtht = ptr + 2

    densityLeft = density - Decimal(0.005)
    densityRight = density + Decimal(0.005)

    analogs = Polymers.objects.values('id', 'shortcode', 'subtype__name', 'plants__name', 'ptr', 'density'). \
        exclude(id=polymerId).filter(subtype__type=type, color=color, ptr__gte=ptrLeft, ptr__lte=ptrRigtht,
                                     density__gte=densityLeft, density__lte=densityRight)

    if len(analogs) == 0:
        return None
    else:
        return analogs


def get_analogs_for_LPP(polymer_id, type, subtype, subtype_name, color, ptr, density):
    """
       Возвращает аналоги для полиэтиленна низкого давления
       :param polymer_id: id марки
       :param type: тип полимера
       :param color: цвет полимера
       :param ptr: ПТР полимера
       :param density: плотность полимера
       :return: QuerySet с аналогами если они есть или None, если аналоги для данного полимера не были найдены
    """

    filters = {
        'subtype__type': type,
        'subtype': subtype,
    }
    excludes = {'id': polymer_id}

    if ptr < 2:
        filters['ptr__gte'] = ptr - 0.5
        filters['ptr__lte'] = ptr + 0.5
    elif ptr >= 2 and ptr < 5:
        filters['ptr__gte'] = ptr - 1
        filters['ptr__lte'] = ptr + 1
    elif ptr >= 5 and ptr < 10:
        filters['ptr__gte'] = ptr - 2
        filters['ptr__lte'] = ptr + 3
    elif ptr >= 10:
        filters['ptr__gte'] = ptr - 2
        filters['ptr__lte'] = ptr + 10

    if 'трубн' in subtype_name or 'кабел' in subtype_name:
        filters['color'] = color
    elif 'эструз' in subtype_name:
        del filters['subtype']
        filters['subtype__name__icontains'] = 'эструз'
    elif 'выдув' in subtype_name:
        del filters['subtype']
        filters['subtype__name__icontains'] = 'выдув'

    analogs = Polymers.objects.values(*DISPLAY_VALUES).exclude(**excludes).filter(**filters)

    if len(analogs) == 0:
        return None
    else:
        return analogs


def get_analogs_for_linnear_poly(polymerId, type, color, copolymer, ptr, density, processing_methods):
    """
          Возвращает аналоги для линейного полиэтилена
          :param polymerId: id марки
          :param type: тип полимера
          :param color: цвет полимера
          :param copolymer: сополимер полимера
          :param ptr: ПТР полимера
          :param density: плотность полимера
          :return: QuerySet с аналогами если они есть или None, если аналоги для данного полимера не были найдены
    """
    if processing_methods:
        if 'экструз' in ','.join(map(str, processing_methods)):
            ptrLeft = ptr - ptr / 5
            ptrRigtht = ptr + ptr / 5
        else:
            ptrLeft = ptr - ptr / 10
            ptrRigtht = ptr + ptr / 10
    else:
        ptrLeft = ptr - 2
        ptrRigtht = ptr + 2

    densityLeft = density - Decimal(0.01)
    densityRight = density + Decimal(0.01)

    analogs = Polymers.objects.values('id', 'shortcode', 'subtype__name', 'plants__name', 'ptr', 'density'). \
        exclude(id=polymerId).filter(subtype__type=type, color=color, copolymer=copolymer,
                                     ptr__gte=ptrLeft, ptr__lte=ptrRigtht,
                                     density__gte=densityLeft, density__lte=densityRight)

    if len(analogs) == 0:
        return None
    else:
        return analogs


def get_analogs_for_polystyrene(polymerId, type, subtype, subtype_name, ptr, t_vika, processing_methods):
    """
            Возвращает аналоги для линейного полиэтилена
            :param polymerId: id марки
            :param type: тип полимера
            :param ptr: ПТР полимера
            :param t_vika: т.Вика
            :return: QuerySet с аналогами если они есть или None, если аналоги для данного полимера не были найдены
    """

    if processing_methods:
        if 'экструз' in ','.join(map(str, processing_methods)):
            ptrLeft = ptr - 2
            ptrRigtht = ptr + 2
        else:
            ptrLeft = ptr - 3
            ptrRigtht = ptr + 3
    else:
        ptrLeft = ptr - 3
        ptrRigtht = ptr + 3

    # t_vikaLeft = t_vika - 5
    # t_vikaRight = t_vika + 5

    analogs = Polymers.objects.values('id', 'shortcode', 'subtype__name', 'plants__name', 'ptr', 'density'). \
        exclude(id=polymerId)

    if 'ударопрочный' in subtype_name:
        analogs = analogs.filter(subtype__type=type, subtype__name__icontains='ударопрочный',
                                 ptr__gte=ptrLeft, ptr__lte=ptrRigtht)
    else:
        analogs = analogs.filter(subtype__type=type, subtype=subtype,
                                 ptr__gte=ptrLeft, ptr__lte=ptrRigtht). \
            exclude(subtype__name__icontains='ударопрочный')

    if len(analogs) == 0:
        return None
    else:
        return analogs


def get_analogs_for_polypropylene(polymerId, type, subtype_name, ptr, processing_methods):
    """
                Возвращает аналоги для полипропилена
                :param polymerId: id марки
                :param type: тип полимера
                :param ptr: ПТР полимера
                :return: QuerySet с аналогами если они есть или None, если аналоги для данного полимера не были найдены
    """
    if processing_methods:
        if 'экструз' in ','.join(map(str, processing_methods)):
            ptrLeft = ptr - ptr / 5
            ptrRigtht = ptr + ptr / 5
        else:
            ptrLeft = ptr - ptr / 10
            ptrRigtht = ptr + ptr / 10
    else:
        ptrLeft = ptr - 2
        ptrRigtht = ptr + 2

    analogs = Polymers.objects.values('id', 'shortcode', 'subtype__name', 'plants__name', 'ptr', 'density'). \
        exclude(id=polymerId)

    if 'гомо' in subtype_name:
        analogs = analogs.filter(subtype__type=type, subtype__name__icontains='гомо',
                                 ptr__gte=ptrLeft, ptr__lte=ptrRigtht)
    else:
        analogs = analogs.filter(subtype__type=type, ptr__gte=ptrLeft, ptr__lte=ptrRigtht).exclude(
            subtype__name__icontains='гомо')

    if analogs:
        return analogs

    return None


def get_analogs_for_ABS_plastic(polymerId, type, color, ptr, processing_methods):
    """
               Возвращает аналоги для АБС пластика
               :param polymerId: id марки
               :param type: тип полимера
               :param color: цвет полимера
               :param ptr: ПТР полимера
               :return: QuerySet с аналогами если они есть или None, если аналоги для данного полимера не были найдены
    """

    if processing_methods:
        if 'экструз' in ','.join(map(str, processing_methods)):
            ptrLeft = ptr - 2
            ptrRigtht = ptr + 2
        else:
            ptrLeft = ptr - 3
            ptrRigtht = ptr + 3
    else:
        ptrLeft = ptr - 3
        ptrRigtht = ptr + 3

    analogs = Polymers.objects.values('id', 'shortcode', 'subtype__name', 'plants__name', 'ptr', 'density'). \
        exclude(id=polymerId).filter(subtype__type=type, color=color, ptr__gte=ptrLeft, ptr__lte=ptrRigtht)

    if len(analogs) == 0:
        return None
    else:
        return analogs


def get_analogs_for_PVC(polymerId, type, ptr, density, t_vika, processing_methods):
    """
                Возвращает аналоги для поливинилхлорида
                :param polymerId: id марки
                :param type: тип полимера
                :param ptr: ПТР полимера
                :param density: плотность полимер
                :param t_vika: т.Вика
                :return: QuerySet с аналогами если они есть или None, если аналоги для данного полимера не были найдены
     """

    analogs = Polymers.objects.values('id', 'shortcode', 'subtype__name', 'plants__name', 'ptr', 'density'). \
        exclude(id=polymerId).filter(subtype__type=type, ptr=ptr, density=density, t_vika=t_vika)

    if len(analogs) == 0:
        return None
    else:
        return analogs


def get_analogs_for_rubber(polymer_id, type, subtype, viscosity_Mooney, diene_content, ethylene_content):
    '''
    :param polymer_id:
    :param type:
    :param subtype:
    :param viscosity_Mooney:
    :param diene_content:
    :param ethylene_content:
    :return:
    '''

    if viscosity_Mooney:
        viscosity_Mooney_left, viscosity_Mooney_right  = viscosity_Mooney - 5, viscosity_Mooney + 5
    else:
        viscosity_Mooney_left, viscosity_Mooney_right = None, None

    if ethylene_content:
        ethylene_content_left, ethylene_content_right = ethylene_content - 5, ethylene_content + 5
    else:
        ethylene_content_left, ethylene_content_right = None, None

    if diene_content:
        diene_content_left, diene_content_right = diene_content - 1.5, diene_content + 1.5
    else:
        diene_content_left, diene_content_right = None, None


    analogs = Polymers.objects.values('id', 'shortcode', 'subtype__name', 'plants__name',
                                      'viscosity_Mooney', 'ethylene_content', 'diene_content'). \
        exclude(id=polymer_id).filter(subtype=subtype,
                                      viscosity_Mooney__gte=viscosity_Mooney_left,
                                      viscosity_Mooney__lte=viscosity_Mooney_right,
                                      ethylene_content__gte=ethylene_content_left,
                                      ethylene_content__lte=ethylene_content_right,
                                      diene_content__gte=diene_content_left,
                                      diene_content__lte=diene_content_right)

    if len(analogs) == 0:
        return None
    else:
        return analogs

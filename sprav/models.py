#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from sprav.search_polym_methods.search_analogs import get_analogs_for_polymer


class Applications(models.Model):
    name = models.CharField(unique=True, max_length=255)
    category = models.ForeignKey('ApplicationCategorys', models.DO_NOTHING, db_column='category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Область применения"
        verbose_name_plural = "Области применения"


class ApplicationCategorys(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория области применения"
        verbose_name_plural = "Категории областей применения"


class Colors(models.Model):
    name = models.CharField(unique=True, max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class Modifications(models.Model):
    name = models.CharField(unique=True, max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Модификация"
        verbose_name_plural = "Модификации"


class Copolymers(models.Model):
    name = models.CharField(unique=True, max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сополимер"
        verbose_name_plural = "Сополимеры"


class ObtainingMethods(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метод получения"
        verbose_name_plural = "Методы получения"


class Plants(models.Model):
    name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    shortname = models.CharField(max_length=45, blank=True, null=True)
    address_street = models.CharField(max_length=45, blank=True, null=True)
    address_house = models.CharField(max_length=45, blank=True, null=True)
    address_city = models.CharField(max_length=45, blank=True, null=True)
    address_state = models.CharField(max_length=45, blank=True, null=True)
    address_post = models.CharField(max_length=45, blank=True, null=True)
    registration_number = models.CharField(max_length=45, blank=True, null=True)
    tax_code = models.CharField(max_length=45, blank=True, null=True)
    contact_person = models.CharField(max_length=45, blank=True, null=True)
    pnone = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class ProcessingMethods(models.Model):
    name = models.CharField(unique=True, max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метод переработки"
        verbose_name_plural = "Методы переработки"


class Subtypes(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='подтип')
    type = models.ForeignKey('Types', models.DO_NOTHING, db_column='type', verbose_name='тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подтип"
        verbose_name_plural = "Подтипы"


class Types(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Polymers(models.Model):
    guid_1c = models.CharField(max_length=40, null=True, blank=True, verbose_name='GUID 1C')
    shortcode = models.CharField('Марка', unique=True, max_length=50)
    subtype = models.ForeignKey(Subtypes, on_delete=models.DO_NOTHING, db_column='subtype', verbose_name='подтип')
    ptr = models.FloatField('ПТР', null=True, blank=True)
    ptr_load = models.FloatField('ПТР нагрузка', null=True, blank=True)
    ptr_temperature = models.IntegerField('ПТР температура', null=True, blank=True)
    density = models.DecimalField('Плотность', max_digits=8, decimal_places=4, blank=True, null=True)
    copolymer = models.ForeignKey(Copolymers, models.DO_NOTHING, db_column='copolymer', blank=True, null=True,
                                  verbose_name='сополимер')
    color = models.ForeignKey(Colors, models.DO_NOTHING, db_column='color', verbose_name='цвет')
    modification = models.ForeignKey(Modifications, models.DO_NOTHING, null=True, blank=True,
                                     verbose_name='модификация')
    relation = models.CharField('Отношение', max_length=8, blank=True, null=True)
    t_vika = models.IntegerField('Температура Вика', null=True, blank=True)
    viscosity_Mooney = models.FloatField('Вязкость Муни', null=True, blank=True)
    copolymer_content = models.IntegerField('Содержание сополимера', blank=True, null=True)
    diene_content = models.FloatField('Содержание этилиденнорборнена', null=True, blank=True)
    ethylene_content = models.FloatField('Содержание этилена', null=True, blank=True)
    applications = models.ManyToManyField(Applications, verbose_name='область применения')
    plants = models.ManyToManyField(Plants, verbose_name='произодитель')
    obtaining_methods = models.ManyToManyField(ObtainingMethods, verbose_name='метод получения')
    processing_methods = models.ManyToManyField(ProcessingMethods, verbose_name='метод переработки')

    class Meta:
        verbose_name = "Полимер"
        verbose_name_plural = "Полимеры"

    @property
    def application(self):
        return self.applications.first().name

    @property
    def plant(self):
        return self.plants.first().name

    @property
    def obt_method(self):
        return self.obtaining_methods.first().name

    @property
    def proc_method(self):
        return self.processing_methods.first().name

    @property
    def analogs(self):
        return get_analogs_for_polymer(self.id)

    def __str__(self):
        return self.shortcode

    def get_full_data(self):
        polymer_data = {'id': self.id,
                        'shortcode': self.shortcode,
                        'subtype__type': self.subtype.type,
                        'subtype__type__name': self.subtype.type.name,
                        'subtype__name': self.subtype.name,
                        'ptr': self.ptr,
                        'ptr_load': self.ptr_load,
                        'ptr_temperature': self.ptr_temperature,
                        'density': self.density,
                        'copolymer__name': self.copolymer.name,
                        'color__name': self.color.name,
                        'relation': self.relation,
                        't_vika': self.t_vika,
                        'viscosity_Mooney': self.viscosity_Mooney,
                        'copolymer_content': self.copolymer_content,
                        'diene_content': self.diene_content,
                        'ethylene_content': self.ethylene_content,
                        'application': self.application,
                        'plant': self.plant,
                        'obt_method': self.obt_method,
                        'proc_method': self.proc_method,
                        'analogs': self.analogs,
                        }

        return polymer_data




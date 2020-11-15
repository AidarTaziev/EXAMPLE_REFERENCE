#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from sprav.models import *

# Create your models here.

class ShipmentConditions(models.Model):
    name = models.CharField("Условия доставки", unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Условия доставки"
        verbose_name_plural = "Условия доставки"

class ShipmentMethods(models.Model):
    name = models.CharField("Метод доставки", unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метод доставки"
        verbose_name_plural = "Методы доставки"

class Managers(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    polymers_types = models.ManyToManyField(Types)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Руководитель отдела"
        verbose_name_plural = "Руководители отдела"

class Orders(models.Model):
    idgoods = models.ForeignKey(Polymers, models.DO_NOTHING, db_column='idgoods', verbose_name="Марка")
    numbers = models.IntegerField("Количество тонн")
    consignee = models.CharField("Компания заказчик", max_length=100)
    shipment_from = models.DateField("Отгрузка с")
    shipment_to = models.DateField("Отгрузка до")
    idshipment_conditions = models.ForeignKey(ShipmentConditions, models.DO_NOTHING, db_column='idshipment_conditions', verbose_name="Условие доставки")
    idshipment_methods = models.ForeignKey(ShipmentMethods, models.DO_NOTHING, db_column='idshipment_methods', verbose_name="Метод доставки")
    address = models.CharField("Адрес", max_length=100)
    contact_name = models.CharField("Контактное лицо", max_length=45)
    contact_phone = models.CharField("Контактный телефон", max_length=15, blank=True)
    contact_email = models.CharField("Контактный email", max_length=45, blank=True, null=True)
    message = models.TextField("Сообщение менеджеру", blank=True)
    order_datetime = models.DateTimeField("Дата заявки", default=datetime.now, blank=True)

    def __str__(self):
        return 'заказ %s - от %s' % (str(self.idgoods), str(self.order_datetime))

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


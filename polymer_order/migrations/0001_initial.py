# Generated by Django 2.1.3 on 2020-04-28 12:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sprav', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Managers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('polymers_types', models.ManyToManyField(to='sprav.Types')),
            ],
            options={
                'verbose_name': 'Руководитель отдела',
                'verbose_name_plural': 'Руководители отдела',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.IntegerField(verbose_name='Количество тонн')),
                ('consignee', models.CharField(max_length=100, verbose_name='Компания заказчик')),
                ('shipment_from', models.DateField(verbose_name='Отгрузка с')),
                ('shipment_to', models.DateField(verbose_name='Отгрузка до')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('contact_name', models.CharField(max_length=45, verbose_name='Контактное лицо')),
                ('contact_phone', models.CharField(blank=True, max_length=15, verbose_name='Контактный телефон')),
                ('contact_email', models.CharField(blank=True, max_length=45, null=True, verbose_name='Контактный email')),
                ('message', models.TextField(blank=True, verbose_name='Сообщение менеджеру')),
                ('order_datetime', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Дата заявки')),
                ('idgoods', models.ForeignKey(db_column='idgoods', on_delete=django.db.models.deletion.DO_NOTHING, to='sprav.Polymers', verbose_name='Марка')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='ShipmentConditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Условия доставки')),
            ],
            options={
                'verbose_name': 'Условия доставки',
                'verbose_name_plural': 'Условия доставки',
            },
        ),
        migrations.CreateModel(
            name='ShipmentMethods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Метод доставки')),
            ],
            options={
                'verbose_name': 'Метод доставки',
                'verbose_name_plural': 'Методы доставки',
            },
        ),
        migrations.AddField(
            model_name='orders',
            name='idshipment_conditions',
            field=models.ForeignKey(db_column='idshipment_conditions', on_delete=django.db.models.deletion.DO_NOTHING, to='polymer_order.ShipmentConditions', verbose_name='Условие доставки'),
        ),
        migrations.AddField(
            model_name='orders',
            name='idshipment_methods',
            field=models.ForeignKey(db_column='idshipment_methods', on_delete=django.db.models.deletion.DO_NOTHING, to='polymer_order.ShipmentMethods', verbose_name='Метод доставки'),
        ),
    ]
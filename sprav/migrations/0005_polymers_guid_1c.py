# Generated by Django 2.1.3 on 2020-08-04 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprav', '0004_auto_20200429_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='polymers',
            name='guid_1c',
            field=models.CharField(max_length=40, null=True, verbose_name='GUID 1C'),
        ),
    ]

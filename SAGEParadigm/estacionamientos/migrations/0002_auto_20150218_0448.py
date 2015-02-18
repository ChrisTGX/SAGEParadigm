# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamientos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estacionamiento',
            name='Esquema_tarifario',
            field=models.CharField(max_length=4, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reservasmodel',
            name='Pagada',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='Tarifa',
            field=models.DecimalField(decimal_places=2, max_digits=6, max_length=50, blank=True, null=True),
            preserve_default=True,
        ),
    ]

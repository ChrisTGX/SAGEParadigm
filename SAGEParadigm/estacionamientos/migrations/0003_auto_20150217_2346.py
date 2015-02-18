# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamientos', '0002_estacionamiento_esquema_tarifario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estacionamiento',
            name='Tarifa',
            field=models.DecimalField(max_digits=6, max_length=50, decimal_places=2, null=True, blank=True),
            preserve_default=True,
        ),
    ]

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
            field=models.CharField(null=True, blank=True, max_length=4),
            preserve_default=True,
        ),
    ]

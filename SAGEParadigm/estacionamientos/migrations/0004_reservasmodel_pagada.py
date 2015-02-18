# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamientos', '0003_auto_20150217_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservasmodel',
            name='Pagada',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]

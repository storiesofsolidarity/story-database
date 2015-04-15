# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_auto_20150303_0135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='location',
            name='county',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=False,
        ),
    ]

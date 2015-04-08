# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20150320_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='anonymous',
            field=models.BooleanField(default=False, help_text=b"Group account like 'Web Anonymous' or 'SMS Anonymous'"),
            preserve_default=True,
        ),
    ]

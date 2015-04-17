# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0007_auto_20150417_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='truncated',
            field=models.BooleanField(default=False, help_text=b'Some legacy stories truncated'),
            preserve_default=True,
        ),
    ]

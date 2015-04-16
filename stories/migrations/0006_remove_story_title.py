# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0005_auto_20150414_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='title',
        ),
    ]

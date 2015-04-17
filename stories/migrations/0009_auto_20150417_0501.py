# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0008_story_truncated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ('-created_at',), 'verbose_name_plural': 'stories'},
        ),
    ]

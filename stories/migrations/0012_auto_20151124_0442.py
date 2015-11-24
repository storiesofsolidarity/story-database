# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0011_story_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'photos', blank=True),
            preserve_default=True,
        ),
    ]

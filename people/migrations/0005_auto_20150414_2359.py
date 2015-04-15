# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_author_anonymous'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='company',
            new_name='employer',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='title',
            new_name='occupation',
        ),
        migrations.AlterField(
            model_name='author',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'author_photo', blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'author_photo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='author',
            name='company',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='author',
            name='title',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name_plural': 'stories'},
        ),
        migrations.AlterField(
            model_name='story',
            name='user',
            field=models.ForeignKey(to='people.Author', null=True),
            preserve_default=True,
        ),
    ]

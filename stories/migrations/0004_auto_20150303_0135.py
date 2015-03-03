# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20150303_0115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='user',
            new_name='author',
        ),
    ]

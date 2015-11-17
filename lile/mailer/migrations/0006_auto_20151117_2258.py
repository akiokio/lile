# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0005_auto_20151103_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='status',
            field=models.CharField(default=1, max_length=1, choices=[(b'1', b'Registered'), (b'2', b'Opt-out')]),
        ),
    ]

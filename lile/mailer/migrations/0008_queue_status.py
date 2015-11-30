# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0007_auto_20151130_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='status',
            field=models.CharField(default=1, max_length=254, choices=[(b'1', b'Pending'), (b'2', b'Sent')]),
        ),
    ]

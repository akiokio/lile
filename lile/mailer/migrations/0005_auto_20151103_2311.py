# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0004_auto_20151103_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadcontact',
            name='obs',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='leadcontact',
            name='status',
            field=models.CharField(default=1, max_length=254, choices=[(1, b'Pending'), (2, b'Sent'), (3, b'Bounced'), (4, b'Opened'), (5, b'Send error')]),
        ),
    ]

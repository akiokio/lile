# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0006_auto_20151117_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadcontact',
            name='status',
            field=models.CharField(default=1, max_length=254, choices=[(b'1', b'Pending'), (b'2', b'Sent'), (b'3', b'Bounced'), (b'4', b'Opened'), (b'5', b'Send error')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0008_queue_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='plain_content',
        ),
    ]

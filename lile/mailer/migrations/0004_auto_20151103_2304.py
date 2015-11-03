# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0003_auto_20151103_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadcontact',
            name='_html',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leadcontact',
            name='_text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

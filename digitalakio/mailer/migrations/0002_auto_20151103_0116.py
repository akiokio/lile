# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=500)),
                ('content', models.TextField()),
                ('plain_content', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeadContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=254, choices=[(1, b'Pending'), (2, b'Sent'), (3, b'Bounced'), (4, b'Opened')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=254)),
                ('email', models.ForeignKey(to='mailer.Email')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='lead',
            name='id',
        ),
        migrations.AddField(
            model_name='lead',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 3, 1, 16, 25, 178419, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 3, 1, 16, 28, 139200, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(max_length=254, unique=True, serialize=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='queue',
            name='recipients',
            field=models.ManyToManyField(to='mailer.Lead', through='mailer.LeadContact'),
        ),
        migrations.AddField(
            model_name='leadcontact',
            name='queue',
            field=models.ForeignKey(to='mailer.Queue'),
        ),
        migrations.AddField(
            model_name='leadcontact',
            name='recipient',
            field=models.ForeignKey(to='mailer.Lead'),
        ),
    ]

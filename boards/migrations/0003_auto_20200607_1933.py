# Generated by Django 3.0.6 on 2020-06-07 16:33

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20200606_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='title', unique=True),
        ),
    ]

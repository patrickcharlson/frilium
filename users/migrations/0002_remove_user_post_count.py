# Generated by Django 3.0.6 on 2020-05-28 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='post_count',
        ),
    ]

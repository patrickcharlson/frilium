# Generated by Django 3.0.8 on 2020-07-16 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_twitter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='website',
            field=models.URLField(blank=True, max_length=30, verbose_name='Website'),
        ),
    ]

# Generated by Django 3.0.6 on 2020-06-27 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='boards.Topic'),
        ),
        migrations.AddField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
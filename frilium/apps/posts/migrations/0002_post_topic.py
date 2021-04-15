# Generated by Django 3.0.8 on 2021-03-18 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='topics.Topic'),
        ),
    ]
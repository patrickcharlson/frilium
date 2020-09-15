# Generated by Django 3.0.8 on 2020-09-14 09:27

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='Bio')),
                ('location', models.CharField(blank=True, max_length=30, verbose_name='Location')),
                ('gender', models.CharField(choices=[('', 'Not Specified'), ('Male', 'Male'), ('Female', 'Female')], default='', max_length=50, verbose_name='Gender')),
                ('website', models.URLField(blank=True, max_length=30, verbose_name='Website')),
                ('timezone', models.CharField(default='UTC', max_length=32, verbose_name='Time zone')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Real name')),
                ('twitter', models.CharField(blank=True, max_length=20, verbose_name='Twitter handle')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Administrator status')),
                ('is_mod', models.BooleanField(default=False, verbose_name='moderator status')),
                ('birthday', models.DateField(null=True, verbose_name='Birthday')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

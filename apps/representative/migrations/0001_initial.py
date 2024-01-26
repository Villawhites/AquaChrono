# Generated by Django 5.0.1 on 2024-01-26 15:02

import core.custom_fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Nombres')),
                ('last_name', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('rut', core.custom_fields.RutField(max_length=10, null=True, unique=True, verbose_name='Rut')),
                ('email', models.EmailField(max_length=30, null=True)),
                ('phone', models.BigIntegerField(null=True, validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999999999)], verbose_name='Teléfono')),
                ('password_representative', models.CharField(max_length=50, verbose_name='Contraseña')),
            ],
            options={
                'verbose_name': 'Apoderado',
                'verbose_name_plural': 'Apoderados',
            },
        ),
    ]

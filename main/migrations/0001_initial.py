# Generated by Django 4.0.4 on 2023-06-08 21:46

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Tipo de Documento')),
                ('code', models.CharField(max_length=8, verbose_name='Código')),
            ],
            options={
                'verbose_name': 'Tipo de documento',
                'verbose_name_plural': 'Tipos de documento',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre del Departamento')),
                ('dane_code', models.CharField(max_length=3, verbose_name='Código DANE')),
                ('geonames_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Código GeoNames')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre del Municipio')),
                ('dane_code', models.CharField(max_length=3, verbose_name='Código DANE')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name')),
                ('coords_lat', models.FloatField(blank=True, null=True)),
                ('coords_long', models.FloatField(blank=True, null=True)),
                ('geo_location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='main.state', verbose_name='Municipios')),
            ],
            options={
                'verbose_name': 'Municipios',
                'verbose_name_plural': 'Municipios',
                'ordering': ('name',),
            },
        ),
    ]

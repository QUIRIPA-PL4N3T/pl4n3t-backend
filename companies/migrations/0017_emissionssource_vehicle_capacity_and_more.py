# Generated by Django 4.0.4 on 2023-09-27 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0016_emissionssource_factor_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='emissionssource',
            name='vehicle_capacity',
            field=models.FloatField(default=0, verbose_name='Capacidad'),
        ),
        migrations.AddField(
            model_name='emissionssource',
            name='vehicle_efficiency',
            field=models.FloatField(default=0, verbose_name='Capacidad'),
        ),
        migrations.AddField(
            model_name='emissionssource',
            name='vehicle_efficiency_unit',
            field=models.FloatField(default=0, verbose_name='Capacidad'),
        ),
        migrations.AddField(
            model_name='emissionssource',
            name='vehicle_fuel',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Tipo de Combustible'),
        ),
        migrations.AddField(
            model_name='emissionssource',
            name='vehicle_load',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Tipo de Carga'),
        ),
        migrations.AddField(
            model_name='emissionssource',
            name='vehicle_type',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Tipo de Vehículo'),
        ),
    ]

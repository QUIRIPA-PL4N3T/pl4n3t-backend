# Generated by Django 4.0.4 on 2023-06-08 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmissionAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='equipments/')),
            ],
            options={
                'verbose_name': 'Agente Emisor',
                'verbose_name_plural': 'Agentes Emisores',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EmissionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Categoría de Emisión',
                'verbose_name_plural': 'Categorías de Emisiones',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='GreenhouseGas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('acronym', models.CharField(max_length=255, verbose_name='Sigla')),
                ('unit', models.CharField(max_length=255, verbose_name='Unidad de medida')),
            ],
            options={
                'verbose_name': 'Gas de Efecto Invernadero',
                'verbose_name_plural': 'Gases de Efecto Invernadero',
                'ordering': ('name', 'acronym'),
            },
        ),
        migrations.CreateModel(
            name='UnitGreenhouseGasByAgentEmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0, verbose_name='Cantidad de Emisión')),
                ('maximum_allowed_amount', models.FloatField(verbose_name='Cantidad Máxima Permitida')),
                ('emission_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='greenhouse_gases', to='emissions.emissionagent')),
                ('greenhouse_gas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='greenhouse_gases', to='emissions.greenhousegas')),
            ],
            options={
                'verbose_name': 'Unidad de Emisión de GEI por Agente Emisor',
                'verbose_name_plural': 'Unidades de Emisiones de GEI por Agentes emisores',
                'ordering': ('greenhouse_gas__name',),
            },
        ),
        migrations.AddField(
            model_name='emissionagent',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emissions.emissioncategory'),
        ),
    ]

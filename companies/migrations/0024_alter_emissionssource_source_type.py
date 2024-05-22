# Generated by Django 4.0.4 on 2024-05-21 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emissions', '0004_alter_greenhousegasemission_options'),
        ('companies', '0023_emissionssource_emission_factor_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emissionssource',
            name='source_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emission_sources', to='emissions.sourcetype', verbose_name='Tipo de Fuente de Emisión'),
        ),
    ]
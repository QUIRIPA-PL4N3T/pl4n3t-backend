# Generated by Django 4.0.4 on 2023-08-30 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emissions', '0003_rename_factory_type_emissionfactor_factor_type'),
        ('companies', '0013_location_employees'),
    ]

    operations = [
        migrations.AddField(
            model_name='emissionssource',
            name='emission_factor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='emission_sources', to='emissions.factortype', verbose_name='Factor de Emisión'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.4 on 2023-09-25 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emission_source_classifications', '0007_rename_emission_factor_type_emissionsourcegroup_emission_factor_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='emissionsourcegroup',
            name='allow_inventory',
            field=models.BooleanField(default=False, verbose_name='Permitir registro de inventario'),
        ),
    ]

# Generated by Django 4.0.4 on 2024-05-21 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_unitofmeasure_is_enabled'),
        ('companies', '0022_emissionssource_acquired_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emissionssource',
            name='emission_factor_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emission_sources', to='main.unitofmeasure', verbose_name='Unidad por defecto'),
        ),
        migrations.AlterField(
            model_name='emissionssource',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emission_sources', to='companies.location'),
        ),
    ]
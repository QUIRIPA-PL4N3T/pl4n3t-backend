# Generated by Django 4.0.4 on 2023-08-17 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('emissions', '0001_initial'),
        ('emission_source_classifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emissionsourcegroup',
            name='emission_factors',
            field=models.ManyToManyField(blank=True, related_name='emission_source_group', to='emissions.emissionfactor'),
        ),
    ]

# Generated by Django 4.0.4 on 2024-05-29 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emissions', '0008_emissionfactor_application_percentage_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emissionfactorcomponent',
            old_name='parent_factor',
            new_name='emission_factor',
        ),
    ]

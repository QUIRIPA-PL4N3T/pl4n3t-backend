# Generated by Django 4.0.4 on 2023-10-24 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emission_source_classifications', '0010_emissionsourcegroup_form_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='emissionsourcegroup',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='¿Grupo de clasificación activo?'),
        ),
    ]
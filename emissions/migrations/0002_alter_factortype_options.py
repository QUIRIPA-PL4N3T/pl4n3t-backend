# Generated by Django 4.0.4 on 2023-08-24 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emissions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='factortype',
            options={'ordering': ('name',), 'verbose_name': 'Tipo de Factor de Emisión', 'verbose_name_plural': 'Tipo de Factores de Emisión'},
        ),
    ]

# Generated by Django 4.0.4 on 2024-05-23 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companytemplate',
            options={'verbose_name': 'Plantilla de Compañía', 'verbose_name_plural': 'Plantilla2 de Compañía'},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name': 'Reporte', 'verbose_name_plural': 'Reportes'},
        ),
        migrations.AlterModelOptions(
            name='reporttemplate',
            options={'verbose_name': 'Plantilla de Pl4n3t', 'verbose_name_plural': 'Plantilla2 de Pl4n3t'},
        ),
    ]

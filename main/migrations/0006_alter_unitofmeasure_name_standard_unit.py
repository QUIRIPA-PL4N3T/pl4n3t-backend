# Generated by Django 4.0.4 on 2023-06-10 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_unitofmeasure_measure_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitofmeasure',
            name='name_standard_unit',
            field=models.CharField(blank=True, help_text='Nombre de las unidades estándar a las que se puede convertir directamente esta unidad de medidaSi esta variable es NULL, entonces la unidad estándar para este tipo de medida dada por el localcopia de la lista de códigos StandardsUnits.', max_length=64, verbose_name='Nombre de la unidad Estándar'),
        ),
    ]

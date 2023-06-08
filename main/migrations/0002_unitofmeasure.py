# Generated by Django 4.0.4 on 2023-06-08 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='El(los) nombre(s) de una unidad de medida (udm) particular. Los ejemplos incluirían lo siguiente:1) para el área udm - metros cuadrados <br />2) para udm Time - segundos <br />3) para el área udm - metros <br />4) Ángulo udm - grados.', max_length=32, verbose_name='Nombre')),
                ('slug', models.CharField(blank=True, db_index=True, max_length=32, verbose_name='Slug')),
                ('symbol', models.CharField(help_text='El símbolo utilizado para esta unidad de medida, como "ft" para pies o "m" para metro.', max_length=8, verbose_name='Símbolo')),
                ('measure_type', models.CharField(choices=[('', 'Desconocido'), ('AREA', 'Area'), ('LENGTH', 'Longitud'), ('ANGLE', 'Ángulo'), ('TIME', 'Tiempo'), ('VELOCITY', 'Velocidad'), ('VOLUMEN', 'Volumen'), ('SCALE', 'Escala'), ('WEIGHT', 'Peso')], help_text='Tipo de medida', max_length=8, verbose_name='Tipo de Medida')),
                ('name_standard_unit', models.CharField(blank=True, help_text='Nombre de las unidades estándar a las que se puede convertir directamente esta unidad de medidaSi esta variable es NULL, entonces la unidad estándar para este tipo de medida dada por el localcopia de la lista de códigos StandardsUnits.', max_length=8, verbose_name='Nombre de la unidad Estándar')),
                ('scale_to_standard_unit', models.FloatField(blank=True, help_text='Si el sistema de implementación utilizado para este objeto no es compatible con NULL, la escala se establece en 0 es equivalente a NULL tanto para la escala como para el desplazamiento.<br />Si X es la unidad actual y S es la estándar, la escala de dos variables (ToStandardUnit)y offset(ToStandardUnit) se puede usar para hacer la conversión de X a S por:<br />S = compensación + escala*X <br />y, por el contrario, <br />X = (desplazamiento S)/escala', null=True, verbose_name='Escala para la unidad Estándar')),
                ('offset_to_standard_unit', models.FloatField(blank=True, help_text='Consulte scaleToStandardUnit para obtener una descripción. Nuevamente, esta variable es NULL y no es una conversión lineal es posible. Si las dos unidades son solo una escala en diferencia, entonces este número es cero (0). Si el sistema de implementación utilizado para este objeto no es compatible con NULL, entonces el conjunto de escalado a 0 es equivalente a NULL tanto para la escala como para el desplazamiento', null=True, verbose_name='Compensación a la unidad estándar')),
                ('formula', models.CharField(blank=True, help_text='Una fórmula algebraica (probablemente en algún lenguaje de programación) que convierte esta unidad de medida (representada en la fórmula por su uomSymbol) a la norma ISO (representada por su símbolo. Este atributo de miembro no es obligatorio, pero es una pieza valiosa de documentación', max_length=32, verbose_name='Formula')),
            ],
            options={
                'verbose_name': 'Unidad de Medida',
                'verbose_name_plural': 'Unidades de Medida',
                'ordering': ['symbol', 'name'],
            },
        ),
    ]
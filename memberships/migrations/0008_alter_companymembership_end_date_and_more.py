# Generated by Django 4.0.4 on 2024-05-18 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0007_membership_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companymembership',
            name='end_date',
            field=models.DateTimeField(blank=True, help_text='Deje en blanco para membresías ilimitadas.', null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='duration',
            field=models.IntegerField(default=365, help_text='Ingrese -1 para una membresía ilimitada.', verbose_name='Duración en días'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='membership_type',
            field=models.CharField(choices=[('FREE', 'Gratuita'), ('BASIC', 'Básica'), ('PREMIUM', 'Premium'), ('ELITE', 'Elite')], default='FREE', max_length=50, verbose_name='Tipo de Membresía'),
        ),
    ]

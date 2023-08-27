# Generated by Django 4.0.4 on 2023-08-27 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_country_state_country'),
        ('companies', '0005_companyuser_role_alter_companyuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='ciiu_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Código CIIU'),
        ),
        migrations.AddField(
            model_name='company',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.country', verbose_name='País de origen'),
        ),
        migrations.AddField(
            model_name='company',
            name='nit',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='NIT'),
        ),
    ]

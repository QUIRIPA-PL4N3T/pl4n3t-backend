# Generated by Django 4.0.4 on 2024-06-12 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0028_emissionssource_product_operation_requirements_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo Electrónico'),
        ),
        migrations.AddField(
            model_name='member',
            name='status',
            field=models.CharField(choices=[('INVITED', 'Invitado'), ('ACTIVE', 'Activo'), ('REJECTED', 'Rechazado')], default='INVITED', max_length=20, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='companies_roles', to=settings.AUTH_USER_MODEL),
        ),
    ]

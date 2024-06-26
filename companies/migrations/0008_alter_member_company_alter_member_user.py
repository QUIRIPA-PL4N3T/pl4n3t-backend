# Generated by Django 4.0.4 on 2023-08-27 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0007_member_delete_companyuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members_roles', to='companies.company'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies_roles', to=settings.AUTH_USER_MODEL),
        ),
    ]

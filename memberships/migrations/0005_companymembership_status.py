# Generated by Django 4.0.4 on 2024-05-15 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0004_membership_analysis_tools_membership_basic_support_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymembership',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('CANCELED', 'Canceled'), ('EXPIRED', 'Expired')], default='PENDING', max_length=10),
        ),
    ]

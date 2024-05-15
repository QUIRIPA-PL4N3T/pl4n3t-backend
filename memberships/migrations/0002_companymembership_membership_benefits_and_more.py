# Generated by Django 4.0.4 on 2024-05-14 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0020_alter_emissionssource_code_and_more'),
        ('memberships', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('company', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='membership', to='companies.company')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='benefits',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='duration',
            field=models.IntegerField(default=365, help_text='Duración en días'),
        ),
        migrations.AddField(
            model_name='membership',
            name='type',
            field=models.CharField(choices=[('Libre', 'Basic'), ('Básica', 'Basic'), ('Premium', 'Premium'), ('Vip', 'VIP')], default='Libre', max_length=50, verbose_name='Tipo de Membresía'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nombre'),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.AddField(
            model_name='companymembership',
            name='membership',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='memberships.membership'),
        ),
    ]
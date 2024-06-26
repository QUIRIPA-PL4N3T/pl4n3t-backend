# Generated by Django 4.0.4 on 2023-12-19 12:58

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporttemplate',
            name='annexes',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='baseline_year_diagnostic',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='carbon_footprint_determination',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='carbon_footprint_quantification',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='company_description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='conclusions',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='definitions',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='diagnostic_objectives',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='diagnostic_scope',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='emissions_consolidation',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='emissions_consolidation_year',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='emissions_inventory',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='emissions_inventory_exclusions',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='emissions_reduction_recommendations',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='gei_inventory_boundaries',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='intended_use',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='introduction',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='organizational_description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='quantification_methodology',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='report_results',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]

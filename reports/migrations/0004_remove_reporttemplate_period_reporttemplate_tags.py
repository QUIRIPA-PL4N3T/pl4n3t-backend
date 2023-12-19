# Generated by Django 4.0.4 on 2023-12-19 16:58

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('reports', '0003_reporttemplate_fields_ordered_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporttemplate',
            name='period',
        ),
        migrations.AddField(
            model_name='reporttemplate',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
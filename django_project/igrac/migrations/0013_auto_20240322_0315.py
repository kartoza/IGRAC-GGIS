# Generated by Django 3.2.20 on 2024-03-22 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igrac', '0012_sitepreference_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitepreference',
            name='download_readme_text',
            field=models.TextField(blank=True, help_text='Readme text to be included in the download zip file.', null=True),
        ),
        migrations.AddField(
            model_name='sitepreference',
            name='ggmn_download_readme_text',
            field=models.TextField(blank=True, help_text='Readme text to be included in the download zip file of GGMN data type.', null=True),
        ),
    ]
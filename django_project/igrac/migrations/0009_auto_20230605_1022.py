# Generated by Django 3.2.16 on 2023-06-05 10:22

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('layers', '0044_alter_dataset_unique_together'),
        ('igrac', '0008_igracprofile_organization_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitepreference',
            name='ggmn_layer',
            field=models.OneToOneField(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='preference_ggmn_layer',
                to='layers.dataset'
            ),
        ),
        migrations.AddField(
            model_name='sitepreference',
            name='well_and_monitoring_data_layer',
            field=models.OneToOneField(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='preference_well_and_monitoring_data_layer',
                to='layers.dataset'
            ),
        ),
        migrations.CreateModel(
            name='GroundwaterLayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('organisations', django.contrib.postgres.fields.ArrayField(
                    base_field=models.IntegerField(), size=None)),
                ('layer', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='layers.dataset')),
            ],
        )
    ]

# Generated by Django 4.2.5 on 2023-12-28 14:01

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SajilotantraApp', '0010_merge_20231222_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='governmentprofile',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='guidance',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

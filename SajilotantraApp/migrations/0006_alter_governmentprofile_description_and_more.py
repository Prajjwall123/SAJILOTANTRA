# Generated by Django 5.0 on 2023-12-16 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SajilotantraApp', '0005_alter_governmentprofile_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='governmentprofile',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notice_description',
            field=models.TextField(),
        ),
    ]

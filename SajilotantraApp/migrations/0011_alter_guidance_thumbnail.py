# Generated by Django 4.2.7 on 2023-12-22 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SajilotantraApp', '0010_merge_20231222_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidance',
            name='thumbnail',
            field=models.ImageField(upload_to='thumbnails/'),
        ),
    ]
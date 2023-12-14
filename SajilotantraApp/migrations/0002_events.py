# Generated by Django 4.2.5 on 2023-12-13 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SajilotantraApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]

# Generated by Django 3.1.1 on 2021-07-08 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extraction', '0002_auto_20210708_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='feed_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.1.1 on 2021-07-08 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extraction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='asin',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='feed_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

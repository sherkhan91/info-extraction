# Generated by Django 3.1.1 on 2021-07-15 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extraction', '0005_auto_20210715_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='publication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='extraction.publication'),
        ),
    ]

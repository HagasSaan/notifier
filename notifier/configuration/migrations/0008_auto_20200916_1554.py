# Generated by Django 3.1 on 2020-09-16 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0007_auto_20200916_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagefiltermodel',
            name='parameters',
            field=models.JSONField(blank=True, default='{}'),
        ),
    ]

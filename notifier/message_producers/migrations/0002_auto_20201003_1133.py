# Generated by Django 3.1 on 2020-10-03 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_producers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customproducer',
            name='file',
            field=models.FileField(upload_to='default'),
        ),
    ]
# Generated by Django 3.1 on 2020-10-02 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_producers', '0006_customproducer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producermodel',
            name='object_type',
            field=models.CharField(choices=[('GithubRepository', 'GithubRepository'), ('агл: custom_producers/hello.py', 'агл: custom_producers/hello.py')], max_length=100),
        ),
    ]

# Generated by Django 3.1 on 2020-08-22 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProducerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('parameters', models.JSONField()),
                ('object_type', models.CharField(choices=[('GithubRepository', 'GithubRepository')], max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# Generated by Django 4.0 on 2021-12-15 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_person_options_alter_filmwork_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='название'),
        ),
    ]

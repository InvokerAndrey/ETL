# Generated by Django 4.0 on 2021-12-16 08:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_genre_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='certificate',
            field=models.TextField(blank=True, null=True, verbose_name='сертификат'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='creation_date',
            field=models.DateField(blank=True, null=True, verbose_name='дата создания фильма'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='person',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Person'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='rating',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='рейтинг'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='фамилия'),
        ),
    ]
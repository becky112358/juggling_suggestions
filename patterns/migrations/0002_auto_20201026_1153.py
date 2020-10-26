# Generated by Django 3.1.2 on 2020-10-26 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patterns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='difficulty',
            name='max_height_minus_min_height',
            field=models.IntegerField(default=0, editable=False, verbose_name='maximum height - minimum height'),
        ),
        migrations.AlterField(
            model_name='difficulty',
            name='n_objects',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='number of objects'),
        ),
    ]

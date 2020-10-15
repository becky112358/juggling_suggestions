# Generated by Django 3.1.2 on 2020-10-15 15:00

from django.db import migrations, models
import patterns.models


class Migration(migrations.Migration):

    dependencies = [
        ('patterns', '0004_auto_20201015_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pattern',
            name='siteswap',
            field=models.CharField(max_length=200, validators=[patterns.models.validate_siteswap_characters, patterns.models.validate_siteswap_brackets, patterns.models.validate_siteswap_integer_average]),
        ),
    ]

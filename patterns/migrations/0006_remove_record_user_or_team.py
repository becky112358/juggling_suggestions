# Generated by Django 3.1.2 on 2020-10-30 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patterns', '0005_auto_20201026_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='user_or_team',
        ),
    ]

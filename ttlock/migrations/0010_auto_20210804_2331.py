# Generated by Django 3.1.6 on 2021-08-04 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttlock', '0009_auto_20210804_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttlock',
            name='lockId',
            field=models.CharField(max_length=35, verbose_name='Номер замка'),
        ),
    ]

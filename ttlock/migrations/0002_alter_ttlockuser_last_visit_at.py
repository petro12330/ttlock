# Generated by Django 3.2.4 on 2021-07-01 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttlock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttlockuser',
            name='last_visit_at',
            field=models.DateTimeField(help_text='Врея последнего визита.', max_length=40, null=True),
        ),
    ]

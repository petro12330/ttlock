# Generated by Django 3.1.6 on 2021-08-04 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttlock', '0005_ttlockuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttlockuser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ttlockuser',
            name='username',
            field=models.CharField(max_length=40, verbose_name='Имя/Номер пользователя'),
        ),
    ]

# Generated by Django 4.1.6 on 2023-04-06 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Простой пользователь'), (2, 'Студент'), (3, 'Менеждер'), (4, 'Ментор'), (5, 'Копирайтер'), (6, 'Модератор')], default=1, verbose_name='Статус'),
        ),
    ]

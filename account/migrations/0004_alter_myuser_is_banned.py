# Generated by Django 4.1.6 on 2023-04-12 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_myuser_is_banned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='is_banned',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Ограничений нет'), (2, 'Забанен на время'), (3, 'Забанен навсегда')], default=1, verbose_name='Статус на ограничение'),
        ),
    ]

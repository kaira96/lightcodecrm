# Generated by Django 4.1.6 on 2023-02-25 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0008_alter_assignment_due_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Отправлено'), (2, 'Переделать'), (3, 'Выполнено')], default=1),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='due_time',
            field=models.TimeField(default=datetime.time(21, 42, 57, 63576), verbose_name='Время сдачи'),
        ),
    ]
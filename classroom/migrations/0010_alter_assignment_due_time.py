# Generated by Django 4.1.6 on 2023-04-13 21:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0009_alter_assignment_due_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_time',
            field=models.TimeField(default=datetime.time(3, 41, 19, 164877), verbose_name='Время сдачи'),
        ),
    ]

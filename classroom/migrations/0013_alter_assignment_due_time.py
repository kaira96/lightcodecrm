# Generated by Django 4.1.6 on 2023-02-28 10:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0012_alter_assignment_due_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_time',
            field=models.TimeField(default=datetime.time(16, 14, 20, 759669), verbose_name='Время сдачи'),
        ),
    ]
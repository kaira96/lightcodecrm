# Generated by Django 4.1.6 on 2023-02-23 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('srm', '0006_alter_student_format_alter_student_studying_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='is_prepayment',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='prepayment',
        ),
    ]

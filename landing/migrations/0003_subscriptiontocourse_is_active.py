# Generated by Django 4.1.6 on 2023-03-04 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_alter_stream_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiontocourse',
            name='is_active',
            field=models.BooleanField(default=1, verbose_name='Актуально?'),
            preserve_default=False,
        ),
    ]

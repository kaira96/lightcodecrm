# Generated by Django 4.1.6 on 2023-04-12 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_myuser_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_banned',
            field=models.BooleanField(default=False, verbose_name='Ограниченный доступ'),
        ),
    ]
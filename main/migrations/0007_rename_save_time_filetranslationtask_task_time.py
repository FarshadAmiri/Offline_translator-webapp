# Generated by Django 4.2.6 on 2025-03-12 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_speechtranslationtask'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filetranslationtask',
            old_name='save_time',
            new_name='task_time',
        ),
    ]

# Generated by Django 4.2.6 on 2025-02-03 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[('fa', 'Farsi'), ('en', 'English'), ('ar', 'Arabic'), ('he', 'Hebrew')], max_length=2, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AddField(
            model_name='user',
            name='allowed_langs',
            field=models.ManyToManyField(blank=True, to='users.language'),
        ),
    ]

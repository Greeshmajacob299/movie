# Generated by Django 4.2.15 on 2024-08-21 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_admintable_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admintable',
            name='confirmpassword',
        ),
    ]
# Generated by Django 4.2.6 on 2023-12-07 02:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_comment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Discussion',
        ),
    ]
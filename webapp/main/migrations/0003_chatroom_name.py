# Generated by Django 4.2.6 on 2023-11-09 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_chatroom_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='name',
            field=models.CharField(default='Default Name', max_length=255),
            preserve_default=False,
        ),
    ]

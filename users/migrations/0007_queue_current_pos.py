# Generated by Django 4.2.7 on 2023-11-21 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_queue_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='current_pos',
            field=models.IntegerField(default=0),
        ),
    ]

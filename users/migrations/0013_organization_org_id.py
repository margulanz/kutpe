# Generated by Django 4.2.7 on 2024-04-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_queue_max_service_queue_min_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='org_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-21 08:58

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default=None, max_length=128, region=None, unique=True)),
                ('otp', models.CharField(max_length=6)),
                ('active_until', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
    ]

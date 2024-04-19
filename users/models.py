from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
    photo = models.ImageField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(unique=True, default=None, null=True)
    card_number = models.CharField(max_length=50, null=True, blank=True)


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    joined = models.DateTimeField(auto_now=True)
    position = models.IntegerField(default=None, null=True)
    waiting_time = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} with pos: {self.position}'


class PhoneOTP(models.Model):
    phone_number = PhoneNumberField(unique=True, default=None)
    otp = models.CharField(max_length=6)
    active_until = models.DateTimeField(default=None, null=True, blank=True)


class Organization(models.Model):
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    phone_number = PhoneNumberField(unique=True, default=None, null=True)
    org_id = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.org_id})"


class Queue(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    service_name = models.CharField(
        max_length=100, default="", null=True, unique=True)
    date = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(Participant, null=True, blank=True)
    current_pos = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    num_servers = models.IntegerField(default=2, null=True, blank=True)
    max_service = models.IntegerField(default=20, null=True, blank=True)
    min_service = models.IntegerField(default=10, null=True, blank=True)


class WaitingTime(models.Model):
    waiting_time = models.FloatField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    service_name = models.CharField(
        max_length=100, default="", null=True)
    org_id = models.CharField(max_length=100, null=True, blank=True)

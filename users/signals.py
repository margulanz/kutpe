from .models import User, PhoneOTP
import datetime
from users.utils import generate_otp, send_sms_otp
from django.dispatch import receiver
from django.db.models.signals import post_save
OTP_DEACTIVATE_MIN = 15


def create_and_send_otp(phone_number):
    # delete record with this number if it exists
    if PhoneOTP.objects.filter(phone_number=phone_number).exists():
        PhoneOTP.objects.get(phone_number=phone_number).delete()
    # create otp
    otp = generate_otp()
    # create PhoneOTP instance
    active_until = datetime.datetime.now() + datetime.timedelta(minutes=OTP_DEACTIVATE_MIN)
    phone_otp = PhoneOTP.objects.create(
        phone_number=phone_number, otp=otp, active_until=active_until)
    send_sms_otp(phone_number, otp)


@receiver(post_save, sender=User)
def phone_verification(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        instance.is_active = False
        instance.save()
        phone_number = instance.phone_number
        create_and_send_otp(phone_number)

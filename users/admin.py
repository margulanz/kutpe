from django.contrib import admin
from .models import User, PhoneOTP, Organization, Queue, Participant, WaitingTime
# Register your models here.


class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'otp']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'is_active']


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


class QueueAdmin(admin.ModelAdmin):
    list_display = ['org', 'date']


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'joined', 'position']


class WaitingTimeAdmin(admin.ModelAdmin):
    list_display = ['queue', 'waiting_time', 'date']


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Queue, QueueAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)
admin.site.register(WaitingTime, WaitingTimeAdmin)

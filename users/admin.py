from django.contrib import admin
from .models import User, PhoneOTP, Organization, Queue, Participant
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


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Queue, QueueAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)

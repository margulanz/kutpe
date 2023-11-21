from rest_framework import serializers
from .models import User

import datetime

from django.utils.timezone import make_aware
from django.db.models import Q
from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from allauth.account.adapter import get_adapter
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import authenticate
from allauth.account.utils import setup_user_email
from django.contrib.auth.hashers import check_password
from .models import PhoneOTP


class PhoneOTPSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = PhoneOTP
        exclude = ('active_until',)


class CustomRegisterSerializer(RegisterSerializer):
    phone_number = PhoneNumberField()
    email = serializers.EmailField(required=False)

    def validate_phone_number(self, phone_number):
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                'User with this phone number already exists')
        return phone_number

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['phone_number'] = self.validated_data.get(
            'phone_number', '')
        return cleaned_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)

        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(
                    self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )

        if "phone_number" in self.cleaned_data:
            # You can add code here to save the phone_number to the user model
            user.phone_number = self.cleaned_data['phone_number']
            user.save()

        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class LoginUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            if User.objects.filter(phone_number=phone_number).exists():
                if User.objects.get(phone_number=phone_number).is_active:
                    user = authenticate(request=self.context.get('request'),
                                        phone_number=phone_number, password=password)
                else:
                    msg = {'detail': 'Unable to log in with provided credentials',
                           'register': True}
                    raise serializers.ValidationError(msg)

            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class EmailPhoneUsernameAuthenticationBackend(object):
    @staticmethod
    def authenticate(request, phone_number=None, password=None):
        try:
            user = User.objects.get(
                phone_number=phone_number
            )

        except User.DoesNotExist:
            return None

        if user and check_password(password, user.password):
            return user

        return None

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

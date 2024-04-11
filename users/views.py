from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from allauth.account import app_settings as allauth_account_settings
from dj_rest_auth.app_settings import api_settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import find_nearest_banks, find_nearest_banks_by_location, calculate_time
from .models import Queue, Participant, User
from .serializers import PhoneOTPSerializer
# Create your views here.


class CustomRegisterView(RegisterView):
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if allauth_account_settings.EMAIL_VERIFICATION != \
                allauth_account_settings.EmailVerificationMethod.MANDATORY:
            if api_settings.USE_JWT:
                self.access_token, self.refresh_token = jwt_encode(user)
            elif not api_settings.SESSION_LOGIN:
                # Session authentication isn't active either, so this has to be
                #  token authentication
                api_settings.TOKEN_CREATOR(self.token_model, user, serializer)

        return user


class VerifyPhone(APIView):
    def post(self, request):
        serializer = PhoneOTPSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            print(validated_data)
            try:
                phone_otp = PhoneOTP.objects.get(
                    phone_number=validated_data['phone_number'])
            except:
                return Response("No such phone number", status=status.HTTP_404_NOT_FOUND)

            otp = validated_data['otp']
            current_time = timezone.now()
            if current_time < phone_otp.active_until and phone_otp.otp == otp:
                user = User.objects.get(phone_number=phone_otp.phone_number)
                user.is_active = True
                user.save()
                phone_otp.delete()
                return Response(f"phone number {phone_otp.phone_number} is verified", status=status.HTTP_200_OK)

        return Response("Data is invalid", status=status.HTTP_400_BAD_REQUEST)


class SendOTP(APIView):
    def post(self, request, *args, **kwargs):
        id_ = self.kwargs.get('id', None)
        if id_ and User.objects.filter(id=id_).exists():
            phone_number = User.objects.get(id=id_).phone_number
            create_and_send_otp(phone_number)
            return Response(f"OTP is sent to {phone_number}", status=status.HTTP_200_OK)
        return Response("Data is invalid", status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def add_to_queue(request, queue_id, user_id):
    try:
        queue = Queue.objects.get(id=queue_id)
        user = User.objects.get(id=user_id)
    except:
        return Response(f"Something wrong with request", status=status.HTTP_400_BAD_REQUEST)
    participant = Participant.objects.create(
        user=user, position=queue.count+1, waiting_time=calculate_time()[1])
    # check if empty
    if queue.count == 0:
        queue.current_pos = participant.position
    queue.count += 1
    queue.save()
    queue.participants.add(participant)
    return Response(f"{user} is added to queue with position {participant.position}", status=status.HTTP_200_OK)


@api_view(('POST',))
def process_current_pos(request, queue_id):
    try:
        queue = Queue.objects.get(id=queue_id)
        participant = Participant.objects.get(position=queue.current_pos)
    except:
        return Response(f"Something wrong with request", status=status.HTTP_400_BAD_REQUEST)
    if queue.participants.count():
        queue.current_pos += 1
        queue.save()
        queue.participants.remove(participant)
        participant.delete()
        return Response(f"{participant} was processed and current queue pos is  {queue.current_pos}", status=status.HTTP_200_OK)


class GetNearestBanks(APIView):
    def post(self, request, **kwargs):

        lat = request.data.get('lat')
        lon = request.data.get('lon')
        data = find_nearest_banks(f"{lat},{lon}")
        return Response(data, status=status.HTTP_200_OK)


class GetNearestBanksByLocation(APIView):
    def post(self, request, **kwargs):
        location = request.data.get('location')
        data = find_nearest_banks_by_location(location)
        return Response(data, status=status.HTTP_200_OK)


class GetTime(APIView):
    def post(self, request, **kwargs):
        num_servers = request.data.get('num_servers')
        # inter_arrival_time = request.data.get('inter_arrival_time')
        max_service = request.data.get('max_service')
        min_service = request.data.get('min_service')
        average_l, mean_t = calculate_time(
            num_servers, max_service, min_service)
        return Response({"average_l": average_l, "mean_t": mean_t}, status=status.HTTP_200_OK)

from django.contrib import admin
from django.urls import path, include
from users.views import CustomRegisterView, VerifyPhone, SendOTP, add_to_queue, process_current_pos, GetNearestBanks, GetNearestBanksByLocation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('registration/', CustomRegisterView.as_view(), name='rest_register'),
    path("verify-phone-number/", VerifyPhone.as_view(),
         name='verify_phone_number'),
    path("send-otp/<int:id>/", SendOTP.as_view(), name="send_otp"),
    path("add-to-queue/<int:queue_id>/<int:user_id>",
         add_to_queue, name='add_to_queue'),
    path("process-current-pos/<int:queue_id>",
         process_current_pos, name='process_current_pos'),
    path("get-nearest-banks/", GetNearestBanks.as_view(), name='get_nearest_banks'),
    path("get-nearest-banks-by-location/", GetNearestBanksByLocation.as_view(),
         name='get_nearest_banks_by_location')
]

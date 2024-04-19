from django.contrib import admin
from django.urls import path, include
from users.views import (
    CustomRegisterView,
    VerifyPhone,
    SendOTP,
    add_to_queue,
    process_current_pos,
    GetNearestBanks,
    GetNearestBanksByLocation,
    GetTime,
    GetNearestBanksByLocation,
    GetWaitingTime,
    GetQueue,
    GetUser,
    CreateQueue,
    CreateUser,
    RemoveFromQueue,
    GetUser,
    CreateQueue,
    GetWaitingTimeDay
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("dj_rest_auth.urls")),
    path("registration/", CreateUser.as_view(), name="rest_register"),
    path("verify-phone-number/", VerifyPhone.as_view(),
         name="verify_phone_number"),
    path("send-otp/<int:id>/", SendOTP.as_view(), name="send_otp"),
    path("add-to-queue/<int:org_id>/<int:user_id>",
         add_to_queue, name="add_to_queue"),
    path(
        "process-current-pos/<int:org_id>",
        process_current_pos,
        name="process_current_pos",
    ),
    path("get-nearest-banks/", GetNearestBanks.as_view(), name="get_nearest_banks"),
    path(
        "get-nearest-banks-by-location/",
        GetNearestBanksByLocation.as_view(),
        name="get_nearest_banks_by_location",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc",
         cache_timeout=0), name="schema-redoc"),
    path("get-time/", GetTime.as_view(), name="get_time"),
    path(
        "queue/<int:org_id>/waiting_time/",
        GetWaitingTime.as_view(),
        name="get_waiting_time",
    ),
    path("queue/<int:org_id>/", GetQueue.as_view(), name="get_queue"),
    path(
        "queue/<int:org_id>/remove/<int:user_id>",
        RemoveFromQueue.as_view(),
        name="remove_from_queue",
    ),
    path("get-advice/", GetNearestBanksByLocation.as_view(), name="get_advice"),
    path("user/<int:user_id>/", GetUser.as_view(), name='get_user'),
    path("queue/create/", CreateQueue.as_view(), name="create_queue"),
    path("queue/<int:org_id>/waiting_time_date/",
         GetWaitingTimeDay.as_view(), name="waiting_time_date")
]

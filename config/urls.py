from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("apps.reporting.urls")),
    path("admax/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]

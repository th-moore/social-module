from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls_account")),
    path("settings/", include("accounts.urls_settings")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("forum/", include("forum.urls")),
    path("", include("pages.urls")),
]
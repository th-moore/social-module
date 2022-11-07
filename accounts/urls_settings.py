from django.urls import path

from . import views

app_name = 'settings'


urlpatterns = [
    path('account/', views.account_details, name='account_details'),
    path('adverts/', views.notifications, name='notifications'),
]
from django.urls import path

from . import views

app_name = 'forum'


urlpatterns = [
    # Groups
    path('groups/', views.group_list, name='group_list'),
    # Group
    path('group-join/', views.group_join, name='group_join'),
    path('group/<slug:group>/new-post/', views.post_create, name='post_create'),
    path('group/<slug:group>/', views.group_detail, name='group_detail'),
    # Posts
    path('post/<slug:post>/', views.post_detail, name='post_detail'),
    path('post/<slug:post>/edit/', views.post_update, name='post_update'),
    path('post/<slug:post>/delete/', views.post_delete, name='post_delete'),
    # Events
    path('events/', views.event_list, name='event_list'),
]
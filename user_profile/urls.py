from django.urls import path

from user_profile import views

app_name = 'user-profile'

urlpatterns = [
    path('', views.UserProfile.as_view({'get': 'retrieve'}), name='get-user-profile'),
    path('update/', views.UserProfile.as_view({'patch': 'partial_update'}), name='update-user-profile'),
    path('change_password/', views.PasswordChangeView.as_view({'put': 'update'}), name='change-password'),
]

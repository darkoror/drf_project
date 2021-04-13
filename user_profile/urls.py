from django.urls import path

from user_profile import views

app_name = 'user-profile'

urlpatterns = [
    path('', views.UserProfile.as_view({'get': 'retrieve'}), name='get-user-profile'),
    path('update', views.UserProfile.as_view({'put': 'update',
                                              'patch': 'partial_update'}), name='update-user-profile'),
    path('change_password', views.ChangePassword.as_view(), name='change-password'),
]

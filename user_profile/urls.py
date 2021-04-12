from django.urls import path
from rest_framework.routers import SimpleRouter

from user_profile import views

app_name = 'user-profile'
user_profile_router = SimpleRouter()

urlpatterns = [
    path('', views.UserProfile.as_view({'get': 'retrieve'}), name='get-user-profile'),
    path('update', views.UserProfile.as_view({'put': 'update',
                                              'patch': 'partial_update'}), name='update-user-profile'),
    path('change_password', views.ChangePassword.as_view({'patch': 'partial_update'}), name='change-password'),
]

urlpatterns += user_profile_router.urls

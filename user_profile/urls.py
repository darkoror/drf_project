from django.urls import path
from rest_framework.routers import SimpleRouter

from user_profile import views

app_name = 'user-profile'
user_profile_router = SimpleRouter()
# user_profile_router.register('change_password', views.ChangePassword, basename='change-password')

urlpatterns = [
    path('', views.UserProfile.as_view({'get': 'retrieve'})),
    path('update', views.UserProfile.as_view({'put': 'update',
                                              'patch': 'partial_update'})),
    path('change_password', views.ChangePassword.as_view({'patch': 'partial_update'})),
]

urlpatterns += user_profile_router.urls

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import LogoutView

urlpatterns = [
    # path('register'),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('logout', LogoutView.as_view()),
]

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import SignUpView, ActivateUserView, PasswordResetView, PasswordResetCompleteView

app_name = 'auth'

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name="sign-up"),
    path('activate-user/', ActivateUserView.as_view(), name="activate-user"),
    path('token/', TokenObtainPairView.as_view(), name="obtain-token"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh-token"),
    path('reset-password/', PasswordResetView.as_view(), name="reset-password"),
    path('reset-password-complete/', PasswordResetCompleteView.as_view(), name="reset-password-complete"),
]

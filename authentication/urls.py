from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import SignUpView, EmailVerify, PasswordReset, SetNewPassword

app_name = 'auth'
auth_router = SimpleRouter()

urlpatterns = [
    path('register', SignUpView.as_view(), name="register-user"),
    path('register/email_verify', EmailVerify.as_view(), name="email-verify"),
    path('reset_password', PasswordReset.as_view(), name="reset-password"),
    path('reset_password/set_new_password', SetNewPassword.as_view(), name="set-new-password"),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
]

urlpatterns += auth_router.urls

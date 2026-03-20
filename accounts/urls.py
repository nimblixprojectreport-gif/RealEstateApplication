from django.urls import path
from .views import ForgotPasswordView, ResetPasswordView
from .views import RegisterView
urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("auth/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("auth/reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
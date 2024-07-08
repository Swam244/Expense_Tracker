from .views import *
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register',RegistrationView.as_view(),name="register"),
    path('',LoginView.as_view(),name="login"),
    path('logout',LogoutView.as_view(),name="logout"),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view()),name="validate-username"),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name="validate-email"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name="activate"),
    path('request-reset-link',PasswordResetView.as_view(),name="request-reset-link"),
    path('reset-password/<uidb64>/<token>',CompletePasswordResetView.as_view(),name="reset-user-password"),
]

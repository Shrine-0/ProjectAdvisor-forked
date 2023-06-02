from django.urls import path, include
from users.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, sendPasswordResetEmailView, UserPasswordResetView, UserTokenRefreshView
# , UserLogoutView

urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='Login'),
    path('token/refresh/', UserTokenRefreshView.as_view(), name='token-refresh'),
    # path('logout/', UserLogoutView.as_view(), name='Logout'),
    path('profile/', UserProfileView.as_view(), name='Profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='Change Password'),
    path('resetpasswordemail/', sendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name = "Password_Reset")
]


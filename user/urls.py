from django.urls import path
from .views import LoginView, LogoutView, SignupView, activate
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)
urlpatterns = [
    # Login URL
    path('login/', LoginView.as_view(), name='login'),
    
    # Logout URL
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Signup URL
    path('signup/', SignupView.as_view(), name='register'),
    
    # Email activation URL
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
    # Password reset URL

    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

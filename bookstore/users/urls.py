from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path(
        'password-reset/',
        UserForgotPassword.as_view(),
        name='password_reset',
    ),
    path(
        'set-new-password/<uidb64>/<token>/',
        UserPasswordResetConfirm.as_view(),
        name='password_reset_confirm',
    ),
    path('user/edit/', UserUpdate.as_view(), name='profile_edit'),
    path('user/<str:slug>/', UserDetail.as_view(), name='profile_detail'),
    path('history-user/', views.history_user, name='history_user'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginUser, name='login'),
    path('logout', views.LogoutUser, name='logout'),
    path('signup', views.SignUser, name='signup'),
    path('sign-provider', views.SignProvider, name='signup_provider'),
    path('activate/<uidb64>/<token>/',views.Activation,name="activate"),
    path('forgot-password', views.ForgotPass, name='forgot-password'),
    path('reset-password/<str:id>', views.ResetPass, name='reset-password'),
    path('check', views.Check, name='check_user'),
]

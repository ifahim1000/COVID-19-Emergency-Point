from django.urls import path

from . import views

urlpatterns = [
    path('user', views.UserDashboard, name='user_dashboard'),
    path('provider', views.ProviderDashboard, name='provider_dashboard'),
    path('update', views.UpdateProfile, name='update_profile'),
    path('update-pro', views.UpdateProvider, name='update_provider'),
] 

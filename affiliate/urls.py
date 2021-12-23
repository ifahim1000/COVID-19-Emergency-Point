from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateAff, name="create_affiliate")
]

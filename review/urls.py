from django.urls import path

from . import views

urlpatterns = [
    path('<str:id>', views.WriteReview, name='write_review'),
] 

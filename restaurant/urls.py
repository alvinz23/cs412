from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='restaurant_main'),
    path('order/', views.order, name='restaurant_order'),
    path('confirmation/', views.confirmation, name='restaurant_confirmation'),
]

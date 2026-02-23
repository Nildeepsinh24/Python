from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_buyer/', views.register_buyer, name='register_buyer'),
    path('register_seller/', views.register_seller, name='register_seller'),
    path('add_cattle/', views.add_cattle, name='add_cattle'),
    path('cattle_list/', views.cattle_list, name='cattle_list'),
]

from django.urls import path
from . import  views

urlpatterns = [
   path('', views.gift_finder, name='gift_finder'),
   path('index/', views.index, name='tte'),
]

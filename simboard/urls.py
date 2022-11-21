from django.urls import path
from .views import *


urlpatterns = [
    path('', dash, name='dash'),
    path('orders/', orders, name='orders'),
    path('statistics/', statistics, name='statistics'), 
]

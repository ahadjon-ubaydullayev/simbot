from django.urls import path
from registration.views import index, send_message
from registration import views


urlpatterns = [
    path('api/', index, name='handler'),
    path('orders/send-message/',  send_message, name='send_message'),
   
]

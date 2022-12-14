from django.urls import path
from registration.views import index, send_message
from registration import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/', index, name='handler'),
    path('orders/send-message/',  send_message, name='send_message'),
   
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

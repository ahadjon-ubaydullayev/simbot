from django.urls import path
from registration.views import index


urlpatterns = [
    path('api/', index, name='handler'),
  
   
]

from django.urls import path
from .views import *
from simboard import views


urlpatterns = [
    path('', dash, name='dash'),
    path('orders/', orders, name='orders'),
    # path('orders/',  views.OrderView.as_view(), name='orders'),
    path('orders/create/',  views.CreateOrder.as_view(), name='order_create'),
    path('orders/update/',  views.UpdateOrder.as_view(), name='order_update'),
    path('orders/delete/',  views.DeleteOrder.as_view(), name='order_delete'),
    path('statistics/', statistics, name='statistics'), 

]

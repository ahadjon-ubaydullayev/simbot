from django.shortcuts import render
from registration.models import *
# Create your views here.


def dash(request):
    return render(request, 'navbar.html')

def orders(request):
    orders = SimOrder.objects.all()
    return render(request, 'orders.html', {'orders':orders})

def statistics(request):
    orders = SimOrder.objects.all()
    # daily_orders = SimOrder.objects.filter(added_date=timezone.now)
    # print(daily_orders)
    return render(request, 'statistics.html', {'orders':orders})
from django.shortcuts import render, redirect
from registration.models import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from datetime import datetime
from datetime import date



def dash(request):
    return render(request, 'navbar.html')

# def orders(request):
#     orders = SimOrder.objects.all()
#     return render(request, 'orders/orders.html', {'orders':orders})

def orders(request):
    if request.method == 'POST':
        if 'add_order' in request.POST:
            sim_type = SimCardOption.objects.get(id=request.POST['sim_type'])
            owner = Client.objects.get(id=request.POST['owner'])
            gift = Gift.objects.get(id=request.POST['gift'])
            order_status = OrderStatus.objects.get(id=request.POST['order_status'])
            order = SimOrder.objects.create(
                owner=owner,
                sim_type=sim_type,
                full_name=request.POST['full_name'],
                gift=gift,
                address=request.POST['address'],
                id_picture=request.POST['id_picture'],
                id_picture2=request.POST['id_picture2'],
                tel_number=request.POST['tel_number'],
                order_status=order_status
            )
            
            order.save()
            return redirect('/orders/')
    orders = SimOrder.objects.all()
    clients = Client.objects.all()
    gifts = Gift.objects.all()
    sim_types = SimCardOption.objects.all()
    status = OrderStatus.objects.all()
    return render(request, 'orders/orders.html', {'orders':orders, 'clients':clients, 'sim_types':sim_types, 'gifts':gifts, 'status':status})


def statistics(request):
    orders = SimOrder.objects.all()
    daily_orders = SimOrder.objects.filter(added_date=date.today()).count()
    # delivered_orders = SimOrder.objects.filter(order_status='delivered').count()
    # monthly_orders = SimOrder.objects.filter(added_date=datetime.now().month).count()
    # for i in daily_orders:
    #     daily_income += i.sim_cost
    return render(request, 'statistics.html', 
        {
        'orders':orders, 
        'daily_orders':daily_orders, 
        # 'delivered_orders':delivered_orders
        })
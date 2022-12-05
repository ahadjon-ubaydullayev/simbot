from django.shortcuts import render, redirect
from registration.models import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.views.generic import View, ListView
from datetime import date


def dash(request):
    return render(request, 'navbar.html')


def orders(request):
    orders = SimOrder.objects.all()
    clients = Client.objects.all()
    gifts = Gift.objects.all()
    sim_types = SimCardOption.objects.all()
    status = OrderStatus.objects.all()
    return render(request, 'orders/orders.html', {'orders':orders, 'clients':clients, 'sim_types':sim_types, 'gifts':gifts, 'status':status})


class CreateOrder(View):

    def  get(self, request):
        owner1 = Client.objects.get(id=request.GET.get('owner', None))
        sim_type1 = SimCardOption.objects.get(id=request.GET.get('sim_type', None))
        full_name1 = request.GET.get('full_name', None)
        gift1 = Gift.objects.get(id=request.GET.get('gift', None))
        address1 = request.GET.get('address', None)
        id_picture1 = request.GET.get('id_picture', None)
        id_picture2 = request.GET.get('id_picture2', None)
        tel_number1 = request.GET.get('tel_number', None)
        order_status1 = OrderStatus.objects.get(id=request.GET.get('order_status', None))
        sim_cost1 = 155

        obj = SimOrder.objects.create(
            owner=owner1,
            sim_type=sim_type1,
            full_name=full_name1,
            gift=gift1,
            address=address1,
            id_picture=id_picture1,
            id_picture2=id_picture2,
            tel_number=tel_number1,
            order_status=order_status1,
            sim_cost=sim_cost1,
        )

        order = {
                    'id':obj.id,
                    'sim_type':obj.sim_type.sim_option,
                    'full_name':obj.full_name,
                    'gift':obj.gift.name,
                    'address':obj.address, 
                    'tel_number':obj.tel_number,
                    'order_status':obj.order_status.status_name,
                    'added_date':obj.added_date,
        }
        print(order)
        data = {
            'order': order
        }
        return JsonResponse(data)


class UpdateOrder(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        print("order id: ", id1)
        owner1 = Client.objects.get(id=request.GET.get('owner', None))
        sim_type1 = SimCardOption.objects.get(id=request.GET.get('sim_type', None))
        full_name1 = request.GET.get('full_name', None)
        gift1 = Gift.objects.get(id=request.GET.get('gift', None))
        address1 = request.GET.get('address', None)
        id_picture1 = request.GET.get('id_picture', None)
        id_picture2 = request.GET.get('id_picture2', None)
        tel_number1 = request.GET.get('tel_number', None)
        order_status1 = OrderStatus.objects.get(id=request.GET.get('order_status', None))
        sim_cost1 = 155
        print("details: ", id1, owner1, sim_type1, full_name1, gift1, address1, tel_number1, order_status1)
        obj = SimOrder.objects.get(id=id1)
        obj.id = id1
        obj.owner = owner1
        obj.sim_type = sim_type1
        obj.full_name = full_name1
        obj.gift = gift1
        obj.address = address1
        obj.id_picture = id_picture1
        obj.id_picture2 = id_picture2
        obj.tel_number = tel_number1
        obj.order_status = order_status1
        obj.sim_cost = 132
        obj.save()

        order = {
                    'id':obj.id,
                    'sim_type':obj.sim_type.sim_option,
                    'full_name':obj.full_name,
                    'gift':obj.gift.name,
                    'address':obj.address, 
                    'tel_number':obj.tel_number,
                    'order_status':obj.order_status.status_name,
                    'added_date':obj.added_date
                    }
        print("order: ", order)
        data = {
            'order': order
        }
        return JsonResponse(data)

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

class DeleteOrder(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        print(id1)
        SimOrder.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
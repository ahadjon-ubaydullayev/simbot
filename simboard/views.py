from django.shortcuts import render, redirect
from registration.models import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.views.generic import View, ListView
from datetime import date
import xlwt

 
def dash(request):
    return render(request, 'navbar.html')


def orders(request):
    orders = SimOrder.objects.all()
    clients = Client.objects.all()
    gifts = Gift.objects.all()
    sim_types = SimCardOption.objects.all()
    status = OrderStatus.objects.all()
    messages = MessageToUser.objects.all()
    return render(request, 'orders/orders.html', {'orders':orders, 'clients':clients, 'sim_types':sim_types, 'gifts':gifts, 'status':status, 'messages':messages})


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
        sim_cost1 = sim_type1.cost
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
        obj.save()
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
        data = {
            'order': order
        }
        return JsonResponse(data)


class UpdateOrder(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
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
        data = {
            'order': order
        }
        return JsonResponse(data)

class DeleteOrder(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        SimOrder.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


def month(obj, year=True, day=False):
    this_year = datetime.today().year
    last_year = datetime.today().year-1
    this_month = datetime.today().month
    this_day = datetime.today().day
    res = []
    try:
        if year == True:
            for i in range(1, this_month+1):
                res.append(obj.objects.filter(added_date__year=this_year, added_date__month=i).count())
            return res
        elif day == True:
            for i in range(1, this_day + 1):
                res.append(obj.objects.filter(added_date__year=this_year, added_date__month=this_month, added_date__day=1).count())
            return res
        elif (day == False) and (year == False):
            for i in range(1, this_day + 1):
                res.append(obj.objects.filter(added_date__year=this_year, added_date__month=this_month, added_date__day=i).count())
        else:
            for i in range(1, 13):
                res.append(obj.objects.filter(added_date__year=last_year, added_date__month=i).count())
            return res
    except:
        if year != False:
            for i in range(1, this_month + 1):
                res.append(obj.objects.filter(cr_on__year=this_year, cr_on__month=i).count())
            return res
        elif day == True:
            for i in range(1, this_day + 1):
                res.append(obj.objects.filter(cr_on__year=this_year, cr_on__month=this_month, cr_on__day=i).count())
            return res
        else:
            for i in range(1, 13):
                res.append(obj.objects.filter(cr_on__year=last_year, cr_on__month=i).count())
            return res


def monthly_orders(obj):
    this_year = datetime.today().year
    this_month = datetime.today().month
    this_day = datetime.today().day
    res = []
    res = obj.objects.filter(added_date__year=this_year, added_date__month=this_month).count()
    return res

def daily_income(obj):
    res = 0
    daily_orders = obj.objects.filter(added_date=date.today())
    for order in daily_orders:
        res += order.sim_cost
    return res

def monthly_income(obj):
    this_year = datetime.today().year
    this_month = datetime.today().month
    this_day = datetime.today().day
    res = 0
    orders = obj.objects.filter(added_date__year=this_year, added_date__month=this_month)
    for order in orders:
        res += order.sim_cost
    return res 

def statistics(request):
    orders = SimOrder.objects.all()
    daily_orders = SimOrder.objects.filter(added_date=date.today()).count()
    daily_money = daily_income(SimOrder)
    client_year = month(Client)
    client_l_year = month(Client, year=False)
    client_l_day = month(Client, year=False, day=True)
    order_year = month(SimOrder)
    order_monthly = monthly_orders(SimOrder)
    order_l_year = month(SimOrder, year=False)
    order_l_day = month(SimOrder, year=False, day=True)
    monthly_money = monthly_income(SimOrder)
    delivered_orders = SimOrder.objects.filter(order_status=3).count()
    clients = Client.objects.all().count()
    moths = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'August', 'Sept', 'Oct', 'Nov', 'Dec']
    days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    return render(request, 'statistics.html', {
        'orders': orders,
        'daily_orders': daily_orders,
        'data': [1, 3, 33, 22, 34, 98],
        'last_year': client_l_year,
        'this_year': client_year,
        'order_daily': order_l_day,
        'this_year_order': order_year,
        'order_l_day':order_l_day,
        'day': days,
        'moths': moths,
        'client_l_day': client_l_day,
        'order_monthly':order_monthly,
        'daily_money':daily_money,
        'monthly_money':monthly_money,
        'delivered_orders':delivered_orders,
        'clients':clients
        })





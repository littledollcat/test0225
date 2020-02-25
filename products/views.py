from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import Products, Orders
from django.template import loader
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse

import decimal

from .forms import OrderForm 

import json

# Create your views here.

def index(request):
    query_results = Products.objects.all()
    context = {
        'products': query_results,
        'orders': Orders.objects.all(),
        'form': OrderForm()
    }
    return render(request, 'index.html', context)

def checkVIP(a):
    print('hah')
    
    #a = Products.objects.get(id=1)
    
def create_order(order_detail):
    print('abc')
    #Orders.objects.create(product_id_id=product_id, qty=qty, price=product.price,shop_id=product.shop_id, CustomerID=100.0)

def product(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        product = Products.objects.get(id=product_id)
        vip = 'vip' in request.POST
        print(request.POST)
        
        if (product.vip and vip == product.vip) or not product.vip:
            qty = float(request.POST['qty'])
            if product.stock_pcs >= qty:
                CustomerID = float(request.POST['CustomerID'] or 0)
                print(qty, CustomerID, '**********')
                Orders.objects.create(product_id_id=product_id, qty=qty, price=product.price,shop_id=product.shop_id, CustomerID=CustomerID)

                product.stock_pcs = product.stock_pcs - qty
                product.save()

                return HttpResponseRedirect('./')
            else:
                messages.error(request, '貨源不足')
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, '權限不足')
            return HttpResponseRedirect(reverse('index'))
            

@csrf_exempt
def getTop(request, product_id):
    if request.method == 'POST':
        
        sql = '''
            SELECT * FROM products_orders group by product_id order by qty Limit 3
        '''
        top = [a.product_id.id for a in Orders.objects.raw(sql)]
        
        return HttpResponse(json.dumps({'top':top}), content_type='application/json')

@csrf_exempt
def order(request, order_id):
    print(order_id)
    if request.method == 'DELETE':
        o = Orders.objects.get(id=order_id)
        product = Products.objects.get(id=o.product_id.id)
        print(product.stock_pcs)
        if product.stock_pcs == 0:
            messages.error(request, '商品到貨')
        product.stock_pcs += o.qty
        product.save()
        Orders.objects.filter(id=order_id).delete()
        
        return HttpResponseRedirect(reverse('index'))

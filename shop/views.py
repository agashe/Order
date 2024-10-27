from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Order, OrderItem, Address
from inventory.models import Product
import json

def cart(request):
    title = 'Cart'
    response = JsonResponse({})

    if request.method == "GET":
        if request.GET.get("type") is not None and request.GET.get("type") == 'json':
            response = JsonResponse({
                'cart_items_count': request.COOKIES.get('cart_items_count', 0),
                'cart_total': request.COOKIES.get('cart_total', 0)
            })

            if 'cart_items_count' not in request.COOKIES:
                response.set_cookie('cart_items_count', 0)

            if 'cart_total' not in request.COOKIES:
                response.set_cookie('cart_total', 0)
        else:
            cart_items = request.COOKIES.get('cart_items', '')
            
            items = []
            total = 0
            
            if cart_items != '':
                cart_items = json.loads(cart_items)

                for cart_item in cart_items['data']:
                    items.append({
                        'product': Product.objects.get(id=cart_item['id']),
                        'price': cart_item['price'],
                        'quantity': cart_item['quantity'],
                        'total': cart_item['total']
                    })

                    total += cart_item['total']
            
            response = render(request, "shop/cart.html", {
                'title': title,
                'items': items,
                'total': total,
            })

    elif request.method == "POST" and request.GET.get('action') == 'add':
        response = None

        cart_items_count = int(request.COOKIES.get('cart_items_count', 0))
        cart_total = float(request.COOKIES.get('cart_total', 0))

        if 'cart_items' not in request.COOKIES:
            response = JsonResponse({
                'cart_items_count': cart_items_count,
                'cart_total': cart_total
            })

            response.set_cookie('cart_items', '')
        else:
            cart_items = request.COOKIES.get('cart_items', '')
            item_exists = False

            if cart_items == '':
                cart_items = {
                    'data': [{
                        'id': request.POST.get('id'),
                        'price': request.POST.get('price'),
                        'quantity': request.POST.get('quantity'),
                        'total': int(request.POST.get('quantity')) * float(request.POST.get('price'))
                    }]
                }
            else:
                cart_items = json.loads(cart_items)

                for item in cart_items['data']:
                    if str(item['id']) == request.POST.get('id'):
                       item['quantity'] = int(item['quantity']) + 1
                       item['total'] = (int(item['quantity'])) * float(request.POST.get('price'))
                       item_exists = True 
                       break
                
                if not item_exists:
                    cart_items['data'].append({
                        'id': request.POST.get('id'),
                        'price': request.POST.get('price'),
                        'quantity': request.POST.get('quantity'),
                        'total': int(request.POST.get('quantity')) * float(request.POST.get('price'))
                    })
        
            if not item_exists:
                cart_items_count += 1
                cart_total += int(request.POST.get('quantity')) * float(request.POST.get('price'))
            else:
                cart_total += float(request.POST.get('price'))
            
            response = JsonResponse({
                'cart_items_count': cart_items_count,
                'cart_total': cart_total
            })
                
            response.set_cookie('cart_items', json.dumps(cart_items))
            response.set_cookie('cart_items_count', cart_items_count)
            response.set_cookie('cart_total', cart_total)
        
    elif request.method == "POST" and request.GET.get('action') == 'update': 
            data = request.POST.get('data')

            if data != '':
                cart_items_count = 0
                cart_total = 0
                cart_items = {
                    'data': []
                }

                cart_updated_items = json.loads(data)

                for item in cart_updated_items:    
                    cart_items['data'].append({
                        'id': item['id'],
                        'price': item['price'],
                        'quantity': item['quantity'],
                        'total': int(item['quantity']) * float(item['price'])
                    })
                
                    cart_items_count += 1
                    cart_total += int(item['quantity']) * float(item['price'])

                response = JsonResponse({
                    'cart_items_count': cart_items_count,
                    'cart_total': cart_total,
                    'cart_items': json.dumps(cart_items)
                })
                    
                response.set_cookie('cart_items', json.dumps(cart_items))
                response.set_cookie('cart_items_count', cart_items_count)
                response.set_cookie('cart_total', cart_total)
    
    return response

def checkout(request):
    title = 'Checkout'

    return render(request, "shop/checkout.html", {
        'title': title,
    })

def orders(request):
    title = 'Orders'

    return render(request, "shop/orders.html", {
        'title': title,
    })

def order(request):
    title = 'Order'

    return render(request, "shop/order.html", {
        'title': title,
    })
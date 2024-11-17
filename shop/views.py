from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from .models import Order, OrderItem, Address
from inventory.models import Product
from user.decorators import user_is_auth
from .forms import CheckoutForm
import json
import random

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

@user_is_auth
def checkout(request):
    error = ''

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
    else:
        # redirect to homepage if cart is empty
        return redirect('/')

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        user = request.user

        if form.is_valid():
            if user.address:
                user.address.phone = form.cleaned_data['phone']
                user.address.country = form.cleaned_data['country']
                user.address.state = form.cleaned_data['state']
                user.address.city = form.cleaned_data['city']
                user.address.details = form.cleaned_data['details']
                user.address.postcode = form.cleaned_data['postcode']
                
                user.address.save()
            else:
                address = Address.objects.create(
                    user_id = user.id,
                    phone = form.cleaned_data['phone'],
                    country = form.cleaned_data['country'],
                    state = form.cleaned_data['state'],
                    city = form.cleaned_data['city'],
                    details = form.cleaned_data['details'],
                    postcode = form.cleaned_data['postcode']    
                )

            user.save()

            # create new order , and save its details
            order = Order.objects.create(
                user_id = user.id,
                code = str(random.randint(0, 99999999999)),
                notes = form.cleaned_data['notes'],
                total = total
            )

            for item in items:
                OrderItem.objects.create(
                    order_id = order.id,
                    product_id = item['product'].id,
                    price = item['product'].price,
                    quantity = item['quantity'],
                    total = item['total']
                )

            # empty the cart
            response = redirect('/')
            response.set_cookie('cart_items', json.dumps({
                'data': []
            }))
            
            response.set_cookie('cart_items_count', 0)
            response.set_cookie('cart_total', 0)
        
            messages.success(request, "Your order has been created successfully !")
            return response
        else:
            for error in form.errors.keys():
                if error == 'phone':
                    error = 'Invalid phone !'
                    break
                elif error == 'country':
                    error = 'Invalid country !'
                    break
                elif error == 'state':
                    error = 'Invalid state !'
                    break
                elif error == 'city':
                    error = 'Invalid city !'
                    break
                elif error == 'details':
                    error = 'Invalid address !'
                    break
                
    return render(request, "shop/checkout.html", {
        'title': 'Checkout',
        'items': items,
        'total': total,
        'error': error,
    }) 

def orders(request):
    title = 'Orders'

    paginator = Paginator(request.user.order_set.order_by('-created_at'), 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "shop/orders.html", {
        'title': title,
        'page_obj': page_obj,
    })

def order(request, code):
    order = Order.objects.filter(code=code).first()

    if order is None:
        return redirect('/')

    return render(request, "shop/order.html", {
        'title': 'Order ' + order.code,
        'order': order
    })
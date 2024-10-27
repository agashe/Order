from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category

def index(request):
    title = 'Shop'
    
    if request.GET.get("keyword") is not None:
        products = Product.objects.filter(title__contains=request.GET.get("keyword"))
        title = 'Search Results : ' + request.GET.get("keyword")
        breadcrumbs = [
            {'link': "/products", 'title': 'Shop'},
        ]
    else:
        products = Product.objects.all()
        breadcrumbs = []

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "inventory/index.html", {
        'title': title,
        'page_obj': page_obj,
        'keyword': request.GET.get("keyword"),
        'breadcrumb_items': breadcrumbs
    })

def category(request, id, name):
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category_id=id)

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "inventory/index.html", {
        'title': category.name,
        'page_obj': page_obj,
        'breadcrumb_items': [
            {'link': "/products", 'title': 'Shop'},
        ]
    })

def show(request, id, title):
    product = Product.objects.get(id=id)
    similar_products = Product.objects.exclude(id=id).order_by('?')

    for i in  product.productimage_set.all():
        print(i.image.url)

    return render(request, "inventory/show.html", {
        'title': product.title,
        'product': product,
        'similar_products': similar_products[:4],
        'breadcrumb_items': [
            {'link': "/products", 'title': 'Shop'},
        ]
    })

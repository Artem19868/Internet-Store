from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, ProductGallery
from cart.models import CartItem

# Create your views here.
def is_in_cart(request, product):
        in_cart = False
        cart_item_amount = 0
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(
                cart__user = request.user,
                product = product
            ).first()
            if cart_item:
                in_cart = True
                cart_item_amount = cart_item.amount
        return {
            'in_cart': in_cart,
            'cart_item_amount': cart_item_amount
        }

def paginator(request, product_list, products_per_page):
    product_paginator = Paginator(product_list, products_per_page)
    page = request.GET.get('page')
    paged_products = product_paginator.get_page(page)
    return paged_products

def store(request,category_slug=None):
    if(category_slug):
        all_products = Product.objects.filter(category__slug = category_slug)
    else:
        all_products = Product.objects.all()

    paginated_products = paginator(request, all_products, 6)

    products_list = []
    in_cart_list = []
    amounts_list = []
    for product in paginated_products:
        cart_data = is_in_cart(request, product)
        products_list.append(product)
        in_cart_list.append(cart_data['in_cart'])
        amounts_list.append(cart_data['cart_item_amount'])
    
    products_data = zip(products_list, in_cart_list, amounts_list)

    context = {
        'products_data': products_data,
        'paginated_products': paginated_products
    }
    return render(request,'store/store.html', context)

def detail_view(request, category_slug, product_slug):
    product =  get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug
    )
    product_gallery = ProductGallery.objects.filter(product = product).all()
    cart_data = is_in_cart(request, product)
    context = {
       'product': product,
       'in_cart': cart_data['in_cart'],
       'cart_item_amount': cart_data['cart_item_amount'],
       'product_gallery': product_gallery
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    search_query = request.GET.get('search', '').strip()

    if search_query:
        products = Product.objects.filter(Q(product_name__icontains=search_query), is_available=True).order_by('-product_name')
    else:
        products = Product.objects.filter(is_available=True)

    context = {
        'search_query': search_query,
        'products': products
    }


    return render(request, 'store/store.html', context)
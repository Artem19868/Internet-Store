from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product

# Create your views here.
def paginator(request, product_list, products_per_page):
    product_paginator = Paginator(product_list, products_per_page)
    page = request.GET.get('page')
    paged_products = product_paginator.get_page(page)
    return paged_products

def store(request):
    all_products = Product.objects.all()

    paginated_products = paginator(request, all_products, 6)   

    context = {
        'products': paginated_products
    } 

    return render(request,'store/store.html', context)

def detail_view(request, category_slug, product_slug):
    product =  get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug
    )
    return render(request, 'store/product_detail.html', {'product': product})

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
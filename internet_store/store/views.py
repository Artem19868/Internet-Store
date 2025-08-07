from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Q, Max, QuerySet
from django.contrib.auth.decorators import login_required
from .models import Product, ProductGallery, ReviewRating
from cart.models import CartItem
from category.models import Category

# Create your views here.
def is_in_cart(request, product):
        in_cart = False
        cart_item_amount = 0
        is_purchased = False
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(
                cart__user = request.user,
                product = product
            ).first()
            if cart_item:
                in_cart = True
                cart_item_amount = cart_item.amount
                is_purchased = cart_item.is_purchased
        return {
            'in_cart': in_cart,
            'cart_item_amount': cart_item_amount,
            'is_purchased': is_purchased
        }

def paginator(request, product_list, products_per_page):
    product_paginator = Paginator(product_list, products_per_page)
    page = request.GET.get('page')
    paged_products = product_paginator.get_page(page)
    return paged_products

def products_info(request, products):
    products_list = []
    in_cart_list = []
    amounts_list = []

    for product in products:
        cart_data = is_in_cart(request, product)
        products_list.append(product)
        in_cart_list.append(cart_data['in_cart'])
        amounts_list.append(cart_data['cart_item_amount'])
    products_data = zip(products_list, in_cart_list, amounts_list)
    return products_data

def reviews_rating_info(products):
    if hasattr(products, '__iter__') and not isinstance(products, (str, dict)):
        if isinstance(products, QuerySet) or len(products) == 1:
            # Processing a list of products
            ratings = []
            counts = []
            for product in products:
                ratings.append(Product.avg_review(product))
                counts.append(Product.count_reviews(product))
            return {'rating': ratings, 'count_reviews': counts}
    else:
        # Processing of single product
        return {
            'rating': Product.avg_review(products),
            'count_reviews': Product.count_reviews(products)
        }
    
def custom_page_range(pages_count, active_page_number):
    custom_page_range = 0
        
    if active_page_number >= pages_count-2:
        custom_page_range = range(pages_count-4, pages_count+1)
    elif active_page_number>=5:
        custom_page_range = range(active_page_number-2, active_page_number+3)
    else:
        custom_page_range = range(1, 7)
    return custom_page_range

@login_required(login_url='login')
def store(request,category_slug=None):
    active_page_number = int(request.GET.get('page', 1))
    min_price = 0
    max_price = Product.objects.aggregate(Max('price'))['price__max']

    if(category_slug):
        all_products = Product.objects.filter(category__slug = category_slug)
        if('min_price' in request.GET):
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            products = Product.objects.filter(price__range=(min_price, max_price), category__slug=category_slug, is_available=True).order_by('id')
            paginated_products = paginator(request, products, 4)
            products_data = products_info(request, paginated_products)
        else:
            products = Product.objects.filter(category__slug=category_slug, is_available=True).order_by('id')
            paginated_products = paginator(request, products, 4)
            products_data = products_info(request, paginated_products)
    else:
        if('min_price' in request.GET):
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            if(min_price == ''):
                min_price = 0
            products = Product.objects.filter(price__range=(min_price, max_price), is_available=True).order_by('id')
            paginated_products = paginator(request, products, 4)
            products_data = products_info(request, paginated_products)
        else:
            all_products = Product.objects.all()
            paginated_products = paginator(request, all_products, 4)
            products_data = products_info(request, paginated_products)

    #Custom page range
    pages_count = paginated_products.paginator.num_pages
    page_range = custom_page_range(pages_count, active_page_number)

    context = {
        'products_data': products_data,
        'paginated_products': paginated_products,
        'categories': Category.objects.all(),
        'min_price': min_price,
        'max_price': max_price,
        'active_page_number': active_page_number,
        'max_ellipsis_pagination': pages_count-2,
        'custom_page_range': page_range
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
    reviews_rating_data = reviews_rating_info(product)

    reviews = ReviewRating.objects.filter(product=product, status=True)

    context = {
       'product': product,
       'in_cart': cart_data['in_cart'],
       'cart_item_amount': cart_data['cart_item_amount'],
       'is_purchased': cart_data['is_purchased'],
       'reviews': reviews,
       'reviews_count': reviews_rating_data['count_reviews'],
       'rating': reviews_rating_data['rating'],
       'product_gallery': product_gallery
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    active_page_number = int(request.GET.get('page', 1))
    search_query = request.GET.get('search', '').strip()

    min_price = 0
    max_price = Product.objects.aggregate(Max('price'))['price__max']

    if search_query:
        if('min_price' in request.GET):
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            search_products = Product.objects.filter(Q(product_name__icontains=search_query) | Q(category__category_name__icontains=search_query), is_available=True, price__range=(min_price, max_price)).order_by('-product_name')
            paginated_products = paginator(request, search_products, 4)
            products_data = products_info(request, paginated_products)
        else:
            search_products = Product.objects.filter(Q(product_name__icontains=search_query) | Q(category__category_name__icontains=search_query), is_available=True, price__range=(min_price, max_price)).order_by('-product_name')
            paginated_products = paginator(request, search_products, 4)
            products_data = products_info(request, paginated_products)
    else:
        if('min_price' in request.GET):
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            search_products = Product.objects.filter(is_available=True, price__range=(min_price, max_price)).order_by('-product_name')
            paginated_products = paginator(request, search_products, 4)
            products_data = products_info(request, paginated_products)
        else:
            search_products = Product.objects.filter(is_available=True, price__range=(min_price, max_price)).order_by('-product_name')
            paginated_products = paginator(request, search_products, 4)
            products_data = products_info(request, paginated_products)

    paginated_products = paginator(request, search_products, 4)
    products_data = products_info(request, paginated_products)

    #Custom page range
    pages_count = paginated_products.paginator.num_pages
    page_range = custom_page_range(pages_count, active_page_number)

    context = {
        'search_query': search_query,
        'products_data': products_data,
        'paginated_products': paginated_products,
        'active_page_number': active_page_number,
        'categories': Category.objects.all(),
        'min_price': min_price,
        'max_price': max_price,
        'custom_page_range': page_range
    }
    return render(request, 'store/store.html', context)
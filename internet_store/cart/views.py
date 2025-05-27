from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from store.models import Product
from .models import Cart, CartItem

# Create your views here.
@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    search_query = request.GET.get('search','').strip()
    
    if not cart:
        cart = Cart.objects.create(user=request.user)

    if search_query:
        cart_items = CartItem.objects.filter(Q(product__product_name__icontains=search_query))


    context = {
        'cart_items': cart_items,
        'cart': cart
    }

    return render(request,'cart/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product                             
    )

    if not created:
        cart_item.amount += 1
        cart_item.save()

    return JsonResponse({
        'success': True,
        'product_amount': cart_item.amount,
    })

def remove_from_cart(request, product_id):
    cart_item = CartItem.objects.get(
        cart = Cart.objects.get(user=request.user),
        product = get_object_or_404(Product, id=product_id)
    )
    cart_item.delete()

    return redirect('cart')

@login_required
def amount_in_cart(request, action, product_id):
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(
            cart__user=request.user,
            product=product,
            is_active=True)

    if action == 'plus':
            cart_item.amount += 1
            cart_item.save()
    elif action == 'minus':
            cart_item.amount -= 1
            if cart_item.amount < 1:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'product_amount': 0
                })
            cart_item.save()
    return JsonResponse({
         'success': True,
         'product_amount': cart_item.amount
    })
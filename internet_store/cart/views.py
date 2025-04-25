from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Cart, CartItem

# Create your views here.
@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        cart = Cart.objects.create(user=request.user)

    context = {
        'cart_items': CartItem.objects.all(),
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

    return redirect('cart')

def remove_from_cart(request, product_id):
    cart_item = CartItem.objects.get(
        cart = Cart.objects.get(user=request.user),
        product = get_object_or_404(Product, id=product_id)
    )
    cart_item.delete()

    return redirect('cart')
from django.shortcuts import render
from store.models import Product
from cart.models import Cart, CartItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def buy(request, product_slug):

    user = request.user
    cart = Cart.objects.get(user=user)
    product = get_object_or_404(Product, slug=product_slug)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    
    context = {
        'purchased_product': cart_item
    }
    return render(request,'orders/buy_form.html', context)

    
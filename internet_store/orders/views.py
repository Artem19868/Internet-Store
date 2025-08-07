from django.shortcuts import render, redirect
from store.models import Product, ReviewRating
from store.forms import FormReview
from cart.models import Cart, CartItem
from users.models import Users
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

def write_review(request, product_id):
    form = FormReview(request.POST)
    if form.is_valid():
        url = request.META.get('HTTP_REFERER')
        data = ReviewRating()
        data.rating = form.cleaned_data['rating']
        data.review = form.cleaned_data['review']
        data.product = Product.objects.get(id=product_id)
        data.user = Users.objects.get(id=request.user.id)
        data.save()
    return redirect(url)
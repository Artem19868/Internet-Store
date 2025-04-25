from django.db import models
from users.models import Users
from store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='User')
    date_added = models.DateField(auto_now_add=True, verbose_name='Date added')

    def __str__(self):
        return f'User cart: {self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    

class CartItem(models.Model):
    objects = models.Manager()

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    amount = models.IntegerField( default=1, verbose_name='Amount')
    variations = models.ManyToManyField(Variation, blank=True, verbose_name='Product variations')
    is_active = models.BooleanField(default=True, verbose_name='Is active')

    def __str__(self):
        return f'Product: {self.product}'
    
    def total_price(self):
        return self.product.price * self.amountS

    class Meta:
        verbose_name = 'Cart item'
        verbose_name_plural = 'Cart items'
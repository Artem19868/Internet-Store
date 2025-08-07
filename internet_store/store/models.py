from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count
from category.models import Category
from users.models import Users

# Create your models here.
class Product(models.Model):
    objects = models.Manager()

    amount = models.IntegerField(verbose_name='amount')
    price = models.IntegerField(verbose_name='price')
    product_name = models.CharField(max_length=200, unique=True ,verbose_name='product name')
    slug = models.SlugField(max_length=255, unique=True)
    product_description = models.TextField(verbose_name='product description')
    product_image = models.ImageField(upload_to='main_photos/products', verbose_name='product image')
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='category')
    is_available = models.BooleanField(default=True, verbose_name='is available')

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def avg_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def count_reviews(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = reviews['count']
        return count

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductGallery(models.Model):
    objects = models.Manager()

    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='product')
    image = models.ImageField(upload_to='store/products', max_length=255, verbose_name='image')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'Product photos'
        verbose_name_plural = 'Product gallery'

class VariationManader(models.Manager):

    def sizes(self):
        return super(VariationManader,self).filter(variation_category='size', is_active=True)
    
    def colors(self):
        return super(VariationManader,self).filter(variation_category='color', is_active=True)

variation_category_choice = (
    ('size', 'size'),
    ('color', 'color'),
)

class Variation(models.Model):
    objects = VariationManader()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    variation_category = models.CharField(max_length=100, choices=variation_category_choice, verbose_name='variation_category')
    variation_value = models.CharField(max_length=100, verbose_name='Variation value')
    is_active = models.BooleanField(default=True, verbose_name='Is active')

    def __str__(self):
        return self.variation_value

    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'

class ReviewRating(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, verbose_name='user')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='product')
    review = models.TextField(max_length=400, blank=True, verbose_name='review')
    rating = models.IntegerField(verbose_name='rating')
    status = models.BooleanField(default=True, verbose_name='satus')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    # delete update field
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    def __str__(self):
        return self.review
    class Meta:
        verbose_name = 'Rating and review'
        verbose_name_plural = 'Rating and reviews'